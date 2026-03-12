# 📝 GitHub Issue Creation Best Practices

## Overview

This document explains how the Terraform Auto-Remediation system creates GitHub issues for workflow failures. Issues are **always created in the same repository where the workflow failed**, not in a centralized project.

## ✅ Key Principles

### 1. Same-Repo Creation
- ✅ Issues created in the **same repo** where workflow failed
- ✅ No centralized "issue tracking" repo
- ✅ Developers see issues where they work
- ✅ Issue context stays with the code

### Example:
```
Workflow fails in: your-org/terraform-aws-infra
Issue created in: your-org/terraform-aws-infra  ✅
NOT in:           your-org/centralized-issues  ❌
```

## 🎨 Issue Structure

### Title Format
```
🔥 [AUTO-FIX] Terraform workflow failed: {workflow_name}
```

**Examples:**
- `🔥 [AUTO-FIX] Terraform workflow failed: Terraform CI`
- `🔥 [AUTO-FIX] Terraform workflow failed: Deploy to Production`

### Labels Applied
- `terraform` - Identifies as Terraform-related
- `auto-fix` - Created by automation
- `automated` - Bot-generated
- `infrastructure` - Infrastructure code
- `🤖-bot` - Visual indicator

**Additional labels based on status:**
- `auto-fix-failed` - Fix attempt failed
- `needs-manual-review` - Requires human attention
- `🚨-attention` - High priority

## 📋 Issue Body Sections

### 1. Header Section
```markdown
## 🤖 Automated Terraform Failure Detection

> 🔍 This issue was automatically created by the Terraform Auto-Remediation system.
> The system will attempt to generate and apply a fix automatically.
```

### 2. Failure Details Table
```markdown
| Field | Value |
|-------|-------|
| 🏢 **Repository** | `owner/repo` |
| ⚙️ **Workflow** | `workflow-name` |
| 🔢 **Run ID** | [12345](link) |
| 📅 **Detected At** | 2024-01-01 12:00:00 UTC |
| 🤖 **Handler** | Terraform Auto-Remediation Bot |
```

### 3. Error Message (Expandable)
```markdown
<details>
<summary>Click to expand full error</summary>

```
Error details here...
```

</details>
```

### 4. Status Checklist
```markdown
- [x] 🔍 Failure detected
- [ ] 🧠 AI analysis in progress
- [ ] 🔧 Fix generated
- [ ] ✅ Fix validated
- [ ] 📝 Pull request created
- [ ] 🎉 Issue resolved
```

### 5. What Happens Next
Explains the remediation process step-by-step.

### 6. Configuration
Shows risk thresholds and validation pipeline.

### 7. Related Links
- Workflow run URL
- Documentation
- Troubleshooting guides

### 8. Help Section
Contact information and support resources.

## 🔄 Issue Updates

### When PR is Created
1. **Checkbox updated:**
   ```markdown
   - [x] 📝 Pull request created: [#123](link) 🎉
   ```

2. **PR Details Section Added:**
   ```markdown
   ### 🎉 Pull Request Created!
   
   | Field | Value |
   |-------|-------|
   | 🔗 **PR Number** | [#123](link) |
   | 📝 **Status** | Open and ready for review |
   | 🔔 **Slack** | Team notified |
   | ⏰ **Next Step** | Automatic validation |
   ```

3. **Comment Added:**
   ```markdown
   🎉 **Pull Request Created!**
   
   A fix has been generated: [PR #123](link)
   
   **Next steps:**
   1. Review the PR changes
   2. Run `terraform plan` locally
   3. PR may auto-merge if low risk
   
   cc: @team-members 👀
   ```

### When Fix Fails
1. **Status updated:**
   ```markdown
   - [x] 🔧 Fix generation attempted ❌
   ```

2. **Failure Section Added:**
   ```markdown
   ### ❌ Auto-Fix Failed
   
   **Reason:** AI confidence too low
   
   **What you should do:**
   1. 👨‍💻 Review the error
   2. 🔧 Manually fix
   3. ✅ Close when resolved
   ```

3. **Labels Added:**
   - `auto-fix-failed`
   - `needs-manual-review`
   - `🚨-attention`

4. **Comment Added:**
   ```markdown
   ❌ **Automatic Fix Failed**
   
   **Reason:** {details}
   
   **Action Required:** Manual investigation needed
   ```

## 🎯 Real-World Examples

### Example 1: Successful Auto-Fix

**Issue Created:**
```
Repository: acme-corp/terraform-aws
Title: 🔥 [AUTO-FIX] Terraform workflow failed: Terraform CI
Labels: terraform, auto-fix, automated, infrastructure, 🤖-bot

Status:
- [x] 🔍 Failure detected
- [x] 🧠 AI analysis in progress
- [x] 🔧 Fix generated
- [x] ✅ Fix validated
- [x] 📝 Pull request created: #456 🎉
- [ ] 🎉 Issue resolved
```

**Comments:**
1. Initial creation (by bot)
2. "🎉 Pull Request Created! PR #456" (by bot)
3. "LGTM! Approving" (by human)

**Outcome:** PR merged, issue auto-closed via "Closes #123" in PR

---

### Example 2: Failed Auto-Fix

**Issue Created:**
```
Repository: acme-corp/terraform-gcp
Title: 🔥 [AUTO-FIX] Terraform workflow failed: Deploy Production
Labels: terraform, auto-fix, automated, infrastructure, 🤖-bot, 
        auto-fix-failed, needs-manual-review, 🚨-attention

Status:
- [x] 🔍 Failure detected
- [x] 🧠 AI analysis completed
- [x] 🔧 Fix generation attempted ❌

### ❌ Auto-Fix Failed
Reason: Changes would affect IAM policies (high risk)
```

**Comments:**
1. Initial creation (by bot)
2. "❌ Automatic Fix Failed - Manual review required" (by bot)
3. "@john can you take a look?" (by human)
4. "Fixed in #789" (by human)

**Outcome:** Manually fixed, issue closed by human

---

### Example 3: Low Confidence Fix

**Issue Created:**
```
Repository: acme-corp/terraform-azure
Title: 🔥 [AUTO-FIX] Terraform workflow failed: Validate
Labels: terraform, auto-fix, automated, infrastructure, 🤖-bot,
        auto-fix-failed, needs-manual-review

Status:
- [x] 🔍 Failure detected
- [x] 🧠 AI analysis completed
- [x] 🔧 Fix generation attempted ❌

### ❌ Auto-Fix Failed
Reason: AI confidence 72% (threshold: 85%)

The system determined the error is too complex for safe automatic fixing.
```

**Outcome:** Escalated to team, manually resolved

## 🔍 Issue Discovery

### For Developers
Issues appear in the **same repo** they're working on:

```bash
# Clone your repo
git clone git@github.com:acme-corp/terraform-aws.git
cd terraform-aws

# See issues in GitHub UI
# Navigate to: https://github.com/acme-corp/terraform-aws/issues

# Filter for auto-fixes
# Label: auto-fix
```

### For Platform Team
Monitor all auto-fix issues across repos:

**GitHub Search:**
```
org:acme-corp label:auto-fix is:open
```

**Results:**
- acme-corp/terraform-aws #123 🔥 [AUTO-FIX] Terraform workflow failed
- acme-corp/terraform-gcp #456 🔥 [AUTO-FIX] Terraform workflow failed
- acme-corp/terraform-azure #789 🔥 [AUTO-FIX] Terraform workflow failed

## 📊 Issue Metrics

Track via GitHub API or dashboards:

```python
# Count auto-fix issues
org:acme-corp label:auto-fix

# Success rate
(fixed - failed) / total

# Average time to resolution
closed_at - created_at

# Manual intervention rate
label:needs-manual-review / label:auto-fix
```

## 🎨 Visual Examples

### Successful Issue Lifecycle

```
┌─────────────────────────────────────────┐
│ 🔥 Issue #123 Created                   │
│ Status: Failure detected                │
│ Labels: terraform, auto-fix             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 🧠 AI Analysis in Progress              │
│ Comment: "Analyzing error..."           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 📝 PR #456 Created                      │
│ Comment: "🎉 Pull Request Created!"     │
│ Issue updated with PR link              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ ✅ PR Merged                            │
│ Issue auto-closed (via "Closes #123")   │
│ Status: 🎉 Resolved                     │
└─────────────────────────────────────────┘
```

### Failed Issue Lifecycle

```
┌─────────────────────────────────────────┐
│ 🔥 Issue #789 Created                   │
│ Status: Failure detected                │
│ Labels: terraform, auto-fix             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ ❌ Auto-Fix Failed                      │
│ Label added: auto-fix-failed            │
│ Comment: "Manual review required"       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 👨‍💻 Human Investigation                 │
│ Comment: "Looking into this..."         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ ✅ Manually Fixed                       │
│ Comment: "Fixed in PR #890"             │
│ Issue closed by human                   │
└─────────────────────────────────────────┘
```

## ✅ Best Practices

### DO ✅
- Create issues in the same repo where workflow failed
- Use rich formatting (tables, expandable sections, emojis)
- Include direct links to workflow runs and logs
- Add meaningful labels for filtering
- Update issue status as remediation progresses
- Add comments for major state changes
- Link PR back to issue with "Closes #123"
- Provide clear next steps for humans

### DON'T ❌
- Create issues in a centralized tracking repo
- Use plain text without formatting
- Forget to link to relevant resources
- Leave issues without updates
- Spam with too many comments
- Use unclear or generic titles
- Leave failed issues in limbo

## 🔧 Configuration

The issue creation is handled in:
```python
# src/services/remediation_service.py
async def _create_tracking_issue(
    self,
    repo_owner: str,
    repo_name: str,  # Same repo where workflow failed!
    workflow_name: str,
    error_message: str,
    workflow_run_id: int
):
    # Create issue in the SAME repo
    issue = github_client.create_issue(
        repo_owner, 
        repo_name,  # ← Same repo!
        title, 
        body,
        labels=[...]
    )
```

## 🎉 Summary

✅ Issues created in **same repo** where workflow failed  
✅ Rich formatting with emojis, tables, and links  
✅ Clear status tracking with checkboxes  
✅ Detailed error information and context  
✅ Automatic updates as remediation progresses  
✅ Comments added for major events  
✅ Helpful labels for filtering and discovery  
✅ Guidance for human intervention when needed  

This ensures developers see issues in their repos, context stays with the code, and the entire team has visibility! 🚀
