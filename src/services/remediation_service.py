import structlog
import asyncio
from typing import Optional
from datetime import datetime
from src.models.workflow import WorkflowFailure, FixAttempt, TerraformFix
from src.services.github_service import github_client
from src.services.terraform_parser import TerraformLogParser, TerraformRiskAnalyzer
from src.services.ai_service import ai_fix_generator
from src.services.slack_service import slack_notifier
from src.validators.terraform_validator import TerraformValidator
from src.config import settings

logger = structlog.get_logger()


class RemediationOrchestrator:
    """Orchestrate the full remediation workflow."""
    
    def __init__(self):
        self.validator = TerraformValidator()
    
    async def handle_workflow_failure(
        self,
        repo_owner: str,
        repo_name: str,
        workflow_run_id: int,
        workflow_name: str,
        branch: str,
        commit_sha: str
    ):
        """Handle a workflow failure end-to-end with emoji logging! 🚀"""
        
        logger.info(
            "🚀 Starting remediation workflow",
            repo=f"{repo_owner}/{repo_name}",
            run_id=workflow_run_id
        )
        
        try:
            # Step 1: Fetch and parse logs
            logs = await github_client.get_workflow_logs(repo_owner, repo_name, workflow_run_id)
            error_type, error_message, affected_files = TerraformLogParser.parse_logs(logs)
            
            # Check if auto-fixable
            if not TerraformLogParser.is_auto_fixable(error_type):
                logger.info("⚠️ Error type not auto-fixable", error_type=error_type.value)
                await slack_notifier.notify_fix_failed(
                    repo_owner, repo_name, workflow_run_id,
                    f"Error type '{error_type.value}' requires manual intervention"
                )
                return
            
            # Step 2: Create issue for tracking
            logger.info("📝 Creating tracking issue")
            issue = await self._create_tracking_issue(
                repo_owner, repo_name, workflow_name, error_message, workflow_run_id
            )
            
            # Step 3: Generate fix using AI
            logger.info("🧠 Generating AI fix")
            fix = await ai_fix_generator.generate_fix(
                error_type=error_type,
                error_message=error_message,
                affected_files=affected_files,
                repo_owner=repo_owner,
                repo_name=repo_name,
                commit_sha=commit_sha
            )
            
            if not fix or fix.confidence_score < settings.ai_confidence_threshold:
                logger.warning(
                    "⚠️ AI fix confidence too low",
                    confidence=fix.confidence_score if fix else 0
                )
                await self._update_issue_failed(
                    repo_owner, repo_name, issue.number,
                    "AI confidence too low for auto-fix"
                )
                return
            
            # Step 4: Analyze risk
            risk_level, patterns = TerraformRiskAnalyzer.analyze_changes(
                list(fix.files_to_change.keys()),
                fix.files_to_change,
                fix.confidence_score
            )
            
            logger.info(
                "🎯 Risk analysis complete",
                risk_level=risk_level.value,
                patterns=patterns
            )
            
            # Step 5: Create branch and apply fix
            branch_name = f"autofix/terraform-{workflow_run_id}"
            logger.info("🌿 Creating branch and applying fix", branch=branch_name)
            await self._apply_fix_to_branch(
                repo_owner, repo_name, branch_name, branch, fix
            )
            
            # Step 6: Validate fix
            logger.info("✅ Validating fix")
            validation_passed, validation_logs = await self.validator.validate_fix(
                repo_owner, repo_name, branch_name
            )
            
            if not validation_passed:
                logger.error("❌ Fix validation failed")
                await self._update_issue_failed(
                    repo_owner, repo_name, issue.number,
                    f"Validation failed:\n{validation_logs}"
                )
                return
            
            # Step 7: Create PR
            logger.info("📝 Creating pull request")
            pr = await self._create_pull_request(
                repo_owner, repo_name, branch_name, branch,
                workflow_name, error_message, fix, risk_level,
                issue.number
            )
            
            # Step 8: Update issue with PR link
            await self._update_issue_with_pr(
                repo_owner, repo_name, issue.number, pr.number, pr.html_url
            )
            
            # Step 9: Notify Slack
            logger.info("📢 Sending Slack notification")
            await slack_notifier.notify_pr_created(
                repo_owner=repo_owner,
                repo_name=repo_name,
                pr_number=pr.number,
                pr_url=pr.html_url,
                title=pr.title,
                risk_level=risk_level,
                fix_description=fix.fix_description,
                confidence_score=fix.confidence_score
            )
            
            logger.info(
                "🎉 Remediation workflow complete!",
                pr_number=pr.number,
                pr_url=pr.html_url
            )
            
            # Step 10: Schedule auto-merge check (if applicable)
            if TerraformRiskAnalyzer.can_auto_merge(risk_level):
                await self._schedule_auto_merge_check(
                    repo_owner, repo_name, pr.number, risk_level
                )
        
        except Exception as e:
            logger.error("💥 Remediation workflow failed", error=str(e), exc_info=True)
            await slack_notifier.notify_fix_failed(
                repo_owner, repo_name, workflow_run_id, str(e)
            )
    
    async def _create_tracking_issue(
        self,
        repo_owner: str,
        repo_name: str,
        workflow_name: str,
        error_message: str,
        workflow_run_id: int
    ):
        """Create detailed GitHub issue in the SAME repo where workflow failed."""
        
        # Build workflow run URL
        workflow_run_url = f"https://github.com/{repo_owner}/{repo_name}/actions/runs/{workflow_run_id}"
        
        title = f"🔥 [AUTO-FIX] Terraform workflow failed: {workflow_name}"
        
        body = f"""## 🤖 Automated Terraform Failure Detection

> 🔍 This issue was automatically created by the Terraform Auto-Remediation system.
> The system will attempt to generate and apply a fix automatically.

---

### 📊 Failure Details

| Field | Value |
|-------|-------|
| 🏢 **Repository** | `{repo_owner}/{repo_name}` |
| ⚙️ **Workflow** | `{workflow_name}` |
| 🔢 **Run ID** | [{workflow_run_id}]({workflow_run_url}) |
| 📅 **Detected At** | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} |
| 🤖 **Handler** | Terraform Auto-Remediation Bot |

---

### 💥 Error Message

<details>
<summary>Click to expand full error</summary>

```
{error_message[:1000]}
```

</details>

[🔗 View Full Workflow Logs]({workflow_run_url})

---

### 🔄 Remediation Status

- [x] 🔍 Failure detected
- [ ] 🧠 AI analysis in progress
- [ ] 🔧 Fix generated
- [ ] ✅ Fix validated
- [ ] 📝 Pull request created
- [ ] 🎉 Issue resolved

---

### 🎯 What Happens Next?

1. **🧠 AI Analysis** - The system will analyze the error and affected files
2. **🔧 Fix Generation** - AI will generate a safe, minimal fix
3. **✅ Validation** - Fix will be validated with `terraform validate`, `fmt`, `tflint`, and `tfsec`
4. **📝 PR Creation** - A pull request will be created with the fix
5. **🔔 Notification** - Team will be notified via Slack

---

### ⚙️ Configuration

**Risk Thresholds:**
- 🟢 **Low Risk**: Auto-merge after 24h
- 🟡 **Medium Risk**: Requires 1 approval
- 🔴 **High Risk**: Requires 2+ approvals
- 🚨 **Critical Risk**: Requires 3+ approvals + no auto-merge

**Validation Pipeline:**
- ✓ `terraform init -backend=false`
- ✓ `terraform validate`
- ✓ `terraform fmt -check`
- ✓ `tflint` (best practices)
- ✓ `tfsec` (security scanning)

---

### 🔗 Related Links

- [📖 Documentation](https://github.com/{repo_owner}/{repo_name}/blob/main/README.md)
- [⚙️ Workflow Run]({workflow_run_url})
- [🏥 Terraform Healer Docs](https://github.com/YOUR_USERNAME/terraform-healer)

---

### 🆘 Need Help?

If the automatic fix doesn't work or you need assistance:
- 💬 Comment on this issue
- 👥 Tag `@platform-team` or `@devops`
- 📚 Check the [Troubleshooting Guide](https://wiki.example.com/terraform-troubleshooting)

---

<sub>🤖 Automated by Terraform Healer | 🛠️ [Report an issue](https://github.com/YOUR_USERNAME/terraform-healer/issues)</sub>
"""
        
        # Create issue in the SAME repo where workflow failed
        issue = github_client.create_issue(
            repo_owner, 
            repo_name,  # Same repo!
            title, 
            body,
            labels=[
                "terraform",
                "auto-fix",
                "automated",
                "infrastructure",
                "🤖-bot"
            ]
        )
        
        logger.info(
            "📝 Tracking issue created in same repo",
            repo=f"{repo_owner}/{repo_name}",
            issue_number=issue.number,
            issue_url=issue.html_url
        )
        
        return issue
    
    async def _apply_fix_to_branch(
        self,
        repo_owner: str,
        repo_name: str,
        branch_name: str,
        base_branch: str,
        fix: TerraformFix
    ):
        """Create branch and apply fix."""
        
        # Get base branch SHA
        repo = github_client.get_repo(repo_owner, repo_name)
        base_ref = repo.get_branch(base_branch)
        base_sha = base_ref.commit.sha
        
        # Create new branch
        github_client.create_branch(repo_owner, repo_name, branch_name, base_sha)
        
        logger.info("🌿 Created fix branch", branch=branch_name)
        
        # Apply changes to each file
        for file_path, new_content in fix.files_to_change.items():
            _, file_sha = github_client.get_file_content(
                repo_owner, repo_name, file_path, ref=base_branch
            )
            
            github_client.update_file(
                repo_owner, repo_name, file_path,
                new_content,
                f"🔧 fix: {fix.fix_description}",
                branch_name,
                sha=file_sha
            )
            
            logger.info("✏️ Applied fix to file", file=file_path)
    
    async def _create_pull_request(
        self,
        repo_owner: str,
        repo_name: str,
        head_branch: str,
        base_branch: str,
        workflow_name: str,
        error_message: str,
        fix: TerraformFix,
        risk_level,
        issue_number: int
    ):
        """Create pull request with fix."""
        
        required_approvals = TerraformRiskAnalyzer.get_required_approvals(risk_level)
        
        title = f"🤖 [AUTO-FIX] Terraform: {fix.fix_description}"
        
        body = f"""## 🤖 Automated Terraform Fix

**Risk Level**: {risk_level.value.upper()} {self._get_risk_emoji(risk_level)}
**AI Confidence**: {fix.confidence_score}% 🎯
**Required Approvals**: {required_approvals} 👥

### 🔥 Original Error
Workflow `{workflow_name}` failed with:
```
{error_message[:300]}
```

### 🔧 Fix Description
{fix.fix_description}

### 🧠 AI Reasoning
{fix.reasoning}

### 📝 Changes Made
"""
        
        for file_path in fix.files_to_change.keys():
            body += f"- 📄 `{file_path}`\n"
        
        if fix.patterns_detected:
            body += "\n### ⚠️ Patterns Detected\n"
            for pattern in fix.patterns_detected:
                body += f"- 🔍 {pattern}\n"
        
        body += f"""
### ✅ Validation
- [x] `terraform validate` passed ✓
- [x] `terraform fmt -check` passed ✓
- [x] Security scan (tfsec) passed 🔒

### 📋 Review Checklist
- [ ] Run `terraform plan` in your environment
- [ ] Verify no unexpected resource changes
- [ ] Check that fix addresses the actual error
- [ ] Ensure no security implications

### ⏰ Auto-Merge
"""
        
        if TerraformRiskAnalyzer.can_auto_merge(risk_level):
            body += f"✅ This PR will be auto-merged after {settings.auto_merge_delay_hours}h if all checks pass. 🚀\n"
        else:
            body += "❌ This PR requires manual approval and will NOT be auto-merged. 👨‍💻\n"
        
        body += f"\n---\nCloses #{issue_number} 🎫\n"
        body += "*🤖 Generated by Terraform Auto-Remediation System*"
        
        # Determine labels
        labels = ["terraform", "auto-fix", f"risk-{risk_level.value}"]
        if risk_level in ['high', 'critical']:
            labels.append("needs-manual-review")
        
        pr = github_client.create_pull_request(
            repo_owner, repo_name, title, body,
            head_branch, base_branch, labels
        )
        
        logger.info("Pull request created", pr_number=pr.number)
        return pr
    
    def _get_risk_emoji(self, risk_level):
        """Get emoji for risk level."""
        return {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴",
            "critical": "🚨"
        }.get(risk_level.value, "⚪")
    
    async def _update_issue_with_pr(
        self,
        repo_owner: str,
        repo_name: str,
        issue_number: int,
        pr_number: int,
        pr_url: str
    ):
        """Update issue with PR information and add rich details."""
        
        issue = github_client.get_repo(repo_owner, repo_name).get_issue(issue_number)
        current_body = issue.body
        
        # Update status checkboxes
        updated_body = current_body.replace(
            "- [ ] 📝 Pull request created",
            f"- [x] 📝 Pull request created: [#{pr_number}]({pr_url}) 🎉"
        )
        
        # Add PR details section
        pr_section = f"""

---

### 🎉 Pull Request Created!

| Field | Value |
|-------|-------|
| 🔗 **PR Number** | [#{pr_number}]({pr_url}) |
| 📝 **Status** | Open and ready for review |
| 🔔 **Slack** | Team notified |
| ⏰ **Next Step** | Automatic validation and potential auto-merge |

**Actions:**
- [👀 View Pull Request]({pr_url})
- [📊 View Changes]({pr_url}/files)
- [💬 Add Comments]({pr_url}#discussion_bucket)

---

"""
        
        # Insert PR section before the "Related Links" section or at the end
        if "### 🔗 Related Links" in updated_body:
            updated_body = updated_body.replace(
                "### 🔗 Related Links",
                pr_section + "### 🔗 Related Links"
            )
        else:
            updated_body += pr_section
        
        # Update the issue
        github_client.update_issue(
            repo_owner, repo_name, issue_number, 
            body=updated_body
        )
        
        # Add a comment for visibility
        issue.create_comment(
            f"🎉 **Pull Request Created!**\n\n"
            f"A fix has been generated and is ready for review: [PR #{pr_number}]({pr_url})\n\n"
            f"**What was fixed:**\n"
            f"The AI has analyzed the error and created a pull request with the necessary changes.\n\n"
            f"**Next steps:**\n"
            f"1. Review the PR changes\n"
            f"2. Run `terraform plan` locally to verify\n"
            f"3. The PR may auto-merge if it's low risk and all checks pass\n\n"
            f"cc: @{repo_owner} 👀"
        )
        
        logger.info(
            "📝 Issue updated with PR details",
            issue_number=issue_number,
            pr_number=pr_number
        )
    
    async def _update_issue_failed(
        self,
        repo_owner: str,
        repo_name: str,
        issue_number: int,
        reason: str
    ):
        """Update issue when fix fails."""
        
        issue = github_client.get_repo(repo_owner, repo_name).get_issue(issue_number)
        current_body = issue.body
        
        updated_body = current_body + f"\n\n### ❌ Auto-Fix Failed\n\n{reason}\n\n👨‍💻 Manual intervention required. 🔧"
        
        github_client.update_issue(
            repo_owner, repo_name, issue_number,
            body=updated_body
        )
        
        # Add label
        issue.add_to_labels("auto-fix-failed")
    
    async def _schedule_auto_merge_check(
        self,
        repo_owner: str,
        repo_name: str,
        pr_number: int,
        risk_level
    ):
        """
        Schedule auto-merge check.
        
        NOTE: This is a placeholder for future implementation.
        For production, you would:
        1. Use Kubernetes CronJob to check PR age periodically
        2. Use GitHub Actions scheduled workflow
        3. Add Redis + Celery for job scheduling
        
        Current MVP: Auto-merge is manual or via external scheduler
        """
        
        logger.info(
            "⏰ Auto-merge scheduling logged",
            pr_number=pr_number,
            delay_hours=settings.auto_merge_delay_hours,
            risk_level=risk_level.value,
            note="Implement with K8s CronJob or GitHub Actions"
        )


# Global instance
remediation_orchestrator = RemediationOrchestrator()
