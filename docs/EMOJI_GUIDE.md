# 🎨 Emoji Guide for Terraform Auto-Remediation

This document describes all emojis used throughout the system for consistent visual communication! 🚀

## 📊 Status & State Emojis

### Workflow States
- 🚀 **Starting/Launching** - Beginning a process
- ⚙️ **Processing** - Work in progress
- ✅ **Success** - Completed successfully
- ❌ **Failure** - Failed/Error state
- ⚠️ **Warning** - Attention needed
- 🔄 **Retry** - Retrying operation
- ⏸️ **Paused** - Temporarily stopped
- 🛑 **Stopped** - Permanently stopped

### Progress Indicators
- 🔍 **Detecting** - Scanning/searching
- 🧠 **Analyzing** - AI processing
- 🔧 **Fixing** - Applying changes
- 📝 **Creating** - Creating new resource
- ✏️ **Updating** - Modifying existing
- 🗑️ **Deleting** - Removing resource

## 🎯 Risk Level Emojis

- 🟢 **LOW** - Safe, minimal risk
- 🟡 **MEDIUM** - Moderate risk, review recommended
- 🔴 **HIGH** - Significant risk, approval required
- 🚨 **CRITICAL** - Extreme risk, multiple approvals needed

## 🤖 Bot & Automation Emojis

- 🤖 **Bot** - Automated system
- 🧙 **AI Magic** - AI-powered operation
- ⚡ **Fast** - Quick operation
- 🎯 **Accuracy** - Confidence level
- 🎲 **Uncertain** - Low confidence

## 📦 Resource Type Emojis

### GitHub Resources
- �� **Repository** - GitHub repo
- 🌿 **Branch** - Git branch
- 🔗 **PR** - Pull request
- 🎫 **Issue** - GitHub issue
- 💬 **Comment** - Discussion
- 👤 **User** - Person/account
- 👥 **Team** - Group of people
- 🏢 **Organization** - GitHub org

### Terraform Resources
- 📄 **File** - Terraform file (.tf)
- 🏗️ **Infrastructure** - Infrastructure as code
- ☁️ **Cloud** - Cloud provider
- 🔒 **Security** - Security-related
- 🌐 **Network** - Networking resources
- 💾 **Storage** - Storage resources
- 🖥️ **Compute** - Compute resources

## 🔔 Notification Emojis

### Slack Messages
- 📢 **Announcement** - General notification
- 🔔 **Alert** - Important notification
- 💥 **Breaking** - Critical alert
- 🔥 **Fire** - Urgent issue
- 🎉 **Celebration** - Success milestone
- 👀 **Review** - Needs attention
- ⏰ **Time-based** - Scheduled/timer
- 💡 **Info** - Information/tip

## 🔧 Action Emojis

- 🔧 **Fix** - Repair/correction
- 🛠️ **Tools** - Maintenance
- ⚙️ **Configure** - Configuration
- 📝 **Write** - Create/document
- 📖 **Read** - View/inspect
- 🔄 **Sync** - Synchronize
- 🔁 **Retry** - Try again
- ⏭️ **Skip** - Skip step
- ⏸️ **Pause** - Temporarily stop
- ▶️ **Play** - Start/resume

## 💻 Technical Emojis

- 🐛 **Bug** - Software bug
- 🧪 **Test** - Testing
- 📊 **Metrics** - Data/analytics
- 📈 **Growth** - Improvement
- 📉 **Decline** - Degradation
- 🔐 **Secret** - Credentials
- 🔑 **Key** - Authentication
- 🌍 **Global** - Worldwide/all
- 🏠 **Local** - Local environment

## 🎭 Sentiment Emojis

- 😊 **Happy** - Positive outcome
- 😢 **Sad** - Negative outcome
- 🤔 **Thinking** - Considering
- 😅 **Relief** - Close call
- 💪 **Strong** - Confident
- 🙏 **Please** - Request

## 📱 UI Elements

- ➡️ **Next** - Forward/continue
- ⬅️ **Back** - Return/previous
- ⬆️ **Up** - Increase/upgrade
- ⬇️ **Down** - Decrease/downgrade
- ✓ **Check** - Verified/completed
- ✗ **Cross** - Rejected/failed
- ❓ **Question** - Unknown/help
- ℹ️ **Info** - Information

## 🎯 Example Usage in Code

### Slack Notification
```python
slack.notify(
    title="🤖 🟢 Terraform Auto-Fix PR Created!",
    message="📦 Repository: org/repo\n🎯 Confidence: 95%\n⏰ Auto-merge in 24h"
)
```

### GitHub PR Title
```python
pr_title = f"🤖 [AUTO-FIX] Terraform: {fix_description}"
```

### GitHub Issue Body
```markdown
## 🤖 Automated Terraform Failure Detection

**Workflow**: main.yml ⚙️
**Detected**: 2024-01-01 📅

### 💥 Error Message
...

### 📊 Status
- [x] Failure detected 🔍
- [ ] Fix generated 🔧
- [ ] PR created 📝
```

### Log Messages
```python
logger.info("🚀 Starting remediation workflow")
logger.info("🧠 Generating AI fix")
logger.info("✅ Validation passed")
logger.error("❌ Fix validation failed")
logger.warning("⚠️ AI confidence too low")
```

## 🎨 Best Practices

### ✅ DO
- Use emojis consistently for the same concepts
- Start important messages with emojis for visibility
- Use risk level emojis (🟢🟡🔴🚨) prominently
- Combine emojis for clarity (🤖 🟢 = Bot + Success)
- Use celebration emojis for successes (🎉 ✅ 🚀)

### ❌ DON'T
- Overuse emojis (max 2-3 per line)
- Mix different emojis for same concept
- Use emojis that don't render well everywhere
- Use emojis as the only information
- Forget accessibility - always have text too

## 📋 Common Patterns

### PR Title Pattern
```
�� [AUTO-FIX] {Component}: {Brief Description}
```

### Issue Title Pattern
```
🔥 [AUTO] {Component} failed: {Workflow Name}
```

### Slack Alert Pattern
```
{Emoji} {Status} {Description}
📦 Repo: ...
🎯 Confidence: ...
⏰ Action: ...
```

### Log Message Pattern
```
{Status Emoji} {Action description}, {context}
```

## 🌟 Examples by Scenario

### Scenario: Successful Fix
```
Logs:
🚀 Starting remediation workflow
🔍 Parsing Terraform logs  
🧠 Generating AI fix
🎯 Risk analysis: 🟢 LOW (95% confidence)
�� Creating branch
✅ Validation passed
📝 Creating PR
📢 Slack notification sent
🎉 Remediation complete!

Slack:
🤖 🟢 Terraform Auto-Fix PR Created!
📦 your-org/terraform-infra
🔗 PR #123
🎯 95% confidence
⏰ Auto-merge in 24h

PR Title:
🤖 [AUTO-FIX] Terraform: Add missing instance_type variable

Issue:
🔥 [AUTO] Terraform workflow failed: CI
- [x] Detected 🔍
- [x] Fix generated 🔧  
- [x] PR created 📝 #123
```

### Scenario: High Risk Fix
```
Logs:
🚀 Starting remediation
🧠 Generating fix
⚠️ Risk analysis: 🔴 HIGH - IAM changes detected

Slack:
🤖 🔴 Terraform Auto-Fix PR Created!
⚠️ HIGH RISK CHANGE - Manual review required! ��
📦 your-org/terraform-infra
👥 Requires 2+ approvals
❌ Will NOT auto-merge

PR:
🤖 [AUTO-FIX] Terraform: Update IAM policy
🔴 Risk Level: HIGH
👥 Required Approvals: 2
❌ No auto-merge - manual review required
```

### Scenario: Fix Failed
```
Logs:
🚀 Starting remediation
🧠 Generating fix
❌ Validation failed
💥 Remediation workflow failed

Slack:
❌ 🔥 Failed to auto-fix Terraform workflow
📦 your-org/terraform-infra
💥 Error: terraform validate failed
👨‍💻 Manual intervention required!
```

---

**Remember**: Emojis enhance communication but should never replace clear text! 🎯✨
