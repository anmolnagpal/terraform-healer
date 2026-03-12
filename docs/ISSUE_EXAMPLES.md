# 📸 Visual Examples of GitHub Issues

## Example 1: Issue Just Created (Failure Detected)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ acme-corp/terraform-aws                                          ┃
┃ Issue #456                                                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔥 [AUTO-FIX] Terraform workflow failed: Terraform CI

🏷️ terraform  auto-fix  automated  infrastructure  🤖-bot

───────────────────────────────────────────────────────────────────

🤖 Automated Terraform Failure Detection

> 🔍 This issue was automatically created by the Terraform Auto-Remediation
> system. The system will attempt to generate and apply a fix automatically.

───────────────────────────────────────────────────────────────────

📊 Failure Details

╔═══════════════╦═══════════════════════════════════════════════╗
║ Field         ║ Value                                         ║
╠═══════════════╬═══════════════════════════════════════════════╣
║ 🏢 Repository ║ acme-corp/terraform-aws                       ║
║ ⚙️ Workflow    ║ Terraform CI                                  ║
║ 🔢 Run ID     ║ 1234567890 (link)                            ║
║ 📅 Detected   ║ 2024-03-12 10:30:00 UTC                      ║
║ 🤖 Handler    ║ Terraform Auto-Remediation Bot               ║
╚═══════════════╩═══════════════════════════════════════════════╝

───────────────────────────────────────────────────────────────────

💥 Error Message

▼ Click to expand full error

```
Error: Missing required argument

  on main.tf line 12, in resource "aws_instance" "web":
  12: resource "aws_instance" "web" {

The argument "instance_type" is required, but no definition was found.
```

🔗 View Full Workflow Logs

───────────────────────────────────────────────────────────────────

🔄 Remediation Status

☑ 🔍 Failure detected
☐ 🧠 AI analysis in progress
☐ 🔧 Fix generated
☐ ✅ Fix validated
☐ 📝 Pull request created
☐ 🎉 Issue resolved

───────────────────────────────────────────────────────────────────

🎯 What Happens Next?

1. 🧠 AI Analysis - The system will analyze the error
2. 🔧 Fix Generation - AI will generate a safe fix
3. ✅ Validation - Fix validated with terraform tools
4. 📝 PR Creation - Pull request created with fix
5. 🔔 Notification - Team notified via Slack

───────────────────────────────────────────────────────────────────

💬 Comments (0)

```

---

## Example 2: Issue Updated (PR Created)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ acme-corp/terraform-aws                                          ┃
┃ Issue #456                                                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔥 [AUTO-FIX] Terraform workflow failed: Terraform CI

🏷️ terraform  auto-fix  automated  infrastructure  🤖-bot

───────────────────────────────────────────────────────────────────

🤖 Automated Terraform Failure Detection

> 🔍 This issue was automatically created by the Terraform Auto-Remediation
> system. The system will attempt to generate and apply a fix automatically.

───────────────────────────────────────────────────────────────────

📊 Failure Details

╔═══════════════╦═══════════════════════════════════════════════╗
║ Field         ║ Value                                         ║
╠═══════════════╬═══════════════════════════════════════════════╣
║ 🏢 Repository ║ acme-corp/terraform-aws                       ║
║ ⚙️ Workflow    ║ Terraform CI                                  ║
║ 🔢 Run ID     ║ 1234567890 (link)                            ║
║ 📅 Detected   ║ 2024-03-12 10:30:00 UTC                      ║
║ 🤖 Handler    ║ Terraform Auto-Remediation Bot               ║
╚═══════════════╩═══════════════════════════════════════════════╝

───────────────────────────────────────────────────────────────────

💥 Error Message

▼ Click to expand full error
...

───────────────────────────────────────────────────────────────────

🔄 Remediation Status

☑ 🔍 Failure detected
☑ 🧠 AI analysis in progress
☑ 🔧 Fix generated
☑ ✅ Fix validated
☑ 📝 Pull request created: #789 🎉
☐ 🎉 Issue resolved

───────────────────────────────────────────────────────────────────

🎉 Pull Request Created!

╔═══════════════╦═══════════════════════════════════════════════╗
║ Field         ║ Value                                         ║
╠═══════════════╬═══════════════════════════════════════════════╣
║ 🔗 PR Number  ║ #789 (link)                                   ║
║ 📝 Status     ║ Open and ready for review                     ║
║ 🔔 Slack      ║ Team notified                                 ║
║ ⏰ Next Step  ║ Automatic validation and potential auto-merge ║
╚═══════════════╩═══════════════════════════════════════════════╝

Actions:
• 👀 View Pull Request
• 📊 View Changes
• 💬 Add Comments

───────────────────────────────────────────────────────────────────

💬 Comments (1)

┌───────────────────────────────────────────────────────────────┐
│ 🤖 terraform-bot commented 2 minutes ago                      │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│ 🎉 Pull Request Created!                                     │
│                                                               │
│ A fix has been generated and is ready for review: PR #789    │
│                                                               │
│ What was fixed:                                              │
│ The AI has analyzed the error and created a pull request     │
│ with the necessary changes.                                  │
│                                                               │
│ Next steps:                                                  │
│ 1. Review the PR changes                                     │
│ 2. Run `terraform plan` locally to verify                    │
│ 3. The PR may auto-merge if it's low risk and checks pass    │
│                                                               │
│ cc: @acme-corp 👀                                            │
└───────────────────────────────────────────────────────────────┘

```

---

## Example 3: Issue with Failed Auto-Fix

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ acme-corp/terraform-gcp                                          ┃
┃ Issue #123                                                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔥 [AUTO-FIX] Terraform workflow failed: Deploy Production

🏷️ terraform  auto-fix  automated  infrastructure  🤖-bot  
     auto-fix-failed  needs-manual-review  🚨-attention

───────────────────────────────────────────────────────────────────

🤖 Automated Terraform Failure Detection

> 🔍 This issue was automatically created by the Terraform Auto-Remediation
> system. The system will attempt to generate and apply a fix automatically.

───────────────────────────────────────────────────────────────────

📊 Failure Details

╔═══════════════╦═══════════════════════════════════════════════╗
║ Field         ║ Value                                         ║
╠═══════════════╬═══════════════════════════════════════════════╣
║ 🏢 Repository ║ acme-corp/terraform-gcp                       ║
║ ⚙️ Workflow    ║ Deploy Production                             ║
║ 🔢 Run ID     ║ 9876543210 (link)                            ║
║ 📅 Detected   ║ 2024-03-12 14:15:00 UTC                      ║
║ 🤖 Handler    ║ Terraform Auto-Remediation Bot               ║
╚═══════════════╩═══════════════════════════════════════════════╝

───────────────────────────────────────────────────────────────────

💥 Error Message

▼ Click to expand full error

```
Error: Error creating IAM policy

  on iam.tf line 45, in resource "google_project_iam_policy" "project":
  45: resource "google_project_iam_policy" "project" {

googleapi: Error 403: Permission denied
```

🔗 View Full Workflow Logs

───────────────────────────────────────────────────────────────────

🔄 Remediation Status

☑ 🔍 Failure detected
☑ 🧠 AI analysis completed
☑ 🔧 Fix generation attempted ❌

───────────────────────────────────────────────────────────────────

❌ Auto-Fix Failed

Reason: Changes would affect IAM policies (HIGH risk)

What this means:
The automated system was unable to generate a safe fix for this 
issue. This typically happens when:
• The error requires manual judgment or architectural decisions
• The change would be too risky for automated fixing
• The AI confidence level was below the safety threshold
• Multiple files or complex changes would be required

What you should do:
1. 👨‍💻 Review the error message above
2. 🔍 Check the workflow logs (link)
3. 🔧 Manually fix the Terraform code
4. ✅ Close this issue once resolved

Need help?
• 💬 Ask in Slack #terraform-help
• 📚 Check the Terraform docs
• 👥 Tag @platform-team for assistance

───────────────────────────────────────────────────────────────────

💬 Comments (2)

┌───────────────────────────────────────────────────────────────┐
│ 🤖 terraform-bot commented 5 minutes ago                      │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│ ❌ Automatic Fix Failed                                      │
│                                                               │
│ The system attempted to fix this issue automatically but      │
│ was unsuccessful.                                            │
│                                                               │
│ Reason: Changes would affect IAM policies (HIGH risk)        │
│                                                               │
│ Action Required: This issue needs manual investigation.      │
│                                                               │
│ Please review the error, fix the Terraform code manually,    │
│ and close this issue when resolved.                          │
│                                                               │
│ If you need assistance, please reach out to the platform     │
│ team. 🙋                                                     │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ @john-doe commented 1 minute ago                             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│ Thanks for flagging! This is a known issue with the service  │
│ account permissions. Working on it now.                      │
│                                                               │
│ @platform-team can you help grant the necessary IAM perms?   │
└───────────────────────────────────────────────────────────────┘

```

---

## Example 4: Closed Issue (Successfully Resolved)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ acme-corp/terraform-azure                                        ┃
┃ Issue #999 🟢 CLOSED                                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔥 [AUTO-FIX] Terraform workflow failed: Azure CI

🏷️ terraform  auto-fix  automated  infrastructure  🤖-bot

───────────────────────────────────────────────────────────────────

🤖 Automated Terraform Failure Detection

> 🔍 This issue was automatically created by the Terraform Auto-Remediation
> system. The system will attempt to generate and apply a fix automatically.

───────────────────────────────────────────────────────────────────

📊 Failure Details

╔═══════════════╦═══════════════════════════════════════════════╗
║ Field         ║ Value                                         ║
╠═══════════════╬═══════════════════════════════════════════════╣
║ 🏢 Repository ║ acme-corp/terraform-azure                     ║
║ ⚙️ Workflow    ║ Azure CI                                      ║
║ 🔢 Run ID     ║ 5555555555 (link)                            ║
║ 📅 Detected   ║ 2024-03-11 08:00:00 UTC                      ║
║ 🤖 Handler    ║ Terraform Auto-Remediation Bot               ║
╚═══════════════╩═══════════════════════════════════════════════╝

───────────────────────────────────────────────────────────────────

💥 Error Message
...

───────────────────────────────────────────────────────────────────

🔄 Remediation Status

☑ 🔍 Failure detected
☑ 🧠 AI analysis in progress
☑ 🔧 Fix generated
☑ ✅ Fix validated
☑ 📝 Pull request created: #555 🎉
☑ 🎉 Issue resolved

───────────────────────────────────────────────────────────────────

🎉 Pull Request Created!

╔═══════════════╦═══════════════════════════════════════════════╗
║ Field         ║ Value                                         ║
╠═══════════════╬═══════════════════════════════════════════════╣
║ 🔗 PR Number  ║ #555 (link) ✅ MERGED                        ║
║ 📝 Status     ║ Merged                                        ║
║ 🔔 Slack      ║ Team notified                                 ║
║ ⏰ Completed  ║ 2024-03-11 08:45:00 UTC                      ║
╚═══════════════╩═══════════════════════════════════════════════╝

───────────────────────────────────────────────────────────────────

💬 Comments (2)

┌───────────────────────────────────────────────────────────────┐
│ 🤖 terraform-bot commented 1 day ago                         │
├───────────────────────────────────────────────────────────────┤
│ 🎉 Pull Request Created!                                     │
│ A fix has been generated: PR #555                            │
│ ...                                                           │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ @github-actions bot commented 1 day ago                       │
├───────────────────────────────────────────────────────────────┤
│ ✅ This issue was automatically closed via PR #555           │
│                                                               │
│ The fix has been merged and deployed successfully!           │
└───────────────────────────────────────────────────────────────┘

```

---

## Key Features Highlighted

### ✨ Rich Formatting
- 📊 Tables for structured data
- 📦 Expandable sections for long content
- 🎨 Emojis for visual scanning
- 🔗 Direct links to all resources

### 🏷️ Smart Labeling
- Status labels (auto-fix, automated)
- Risk labels (needs-manual-review)
- Category labels (terraform, infrastructure)
- Visual labels (🤖-bot, 🚨-attention)

### 🔄 Live Updates
- Checkboxes update as work progresses
- New sections added when PR created
- Comments added for major events
- Labels added/removed based on status

### 🎯 Clear Actions
- Direct links to view workflow
- Buttons to access PR
- Clear next steps for humans
- Contact information for help

### 📍 Context Preservation
- All issues in the SAME repo as code
- Full error context preserved
- Links to related resources
- Historical record of automation

---

This visual representation shows exactly how issues look in GitHub! 🎨✨
