# 🤖 GitHub Authentication & Bot User Configuration

## Overview

This document explains which user account the Terraform Auto-Remediation system uses to commit code, create PRs, and interact with GitHub repositories.

## 🔑 Two Authentication Methods

### Option 1: GitHub App (Recommended) ✅

**How it works:**
- Create a GitHub App for your organization
- App acts as a distinct bot user
- Shows as "app-name[bot]" in commits and PRs
- Granular permissions per repository
- Better audit trail

**What users see:**
```
🤖 terraform-remediation[bot] commented 5 minutes ago
🤖 terraform-remediation[bot] created PR #123
✏️  Committed by terraform-remediation[bot]
```

**Setup:**
1. Go to GitHub Organization Settings → Developer settings → GitHub Apps
2. Click "New GitHub App"
3. Name: `terraform-remediation-bot`
4. Homepage URL: Your docs URL
5. Webhook URL: `https://terraform-healer.your-domain.com/webhook/github`
6. Webhook secret: Generate a secure secret
7. **Permissions Required:**
   - Repository permissions:
     - ✅ Contents: Read & Write (for commits)
     - ✅ Issues: Read & Write (for creating/updating issues)
     - ✅ Pull requests: Read & Write (for creating PRs)
     - ✅ Workflows: Read (for accessing logs)
     - ✅ Metadata: Read (required)
   - Subscribe to events:
     - ✅ Workflow run
8. Install app on your organizations

**Configuration:**
```yaml
# k8s/deployment.yaml
GITHUB_APP_ID: "123456"
GITHUB_APP_PRIVATE_KEY_PATH: "/secrets/github-app-key.pem"
GITHUB_WEBHOOK_SECRET: "your-webhook-secret"
```

**Pros:**
- ✅ Shows as "[bot]" - clearly indicates automation
- ✅ Granular permissions
- ✅ Can be installed on multiple orgs
- ✅ Better security (limited scope)
- ✅ Free for public and private repos

**Cons:**
- ⚠️ More complex setup
- ⚠️ Requires org admin access

---

### Option 2: Personal Access Token (PAT) 🔑

**How it works:**
- Use a dedicated bot user account (e.g., @terraform-bot)
- Generate a Personal Access Token
- Bot makes commits as that user
- Shows as regular user in GitHub

**What users see:**
```
👤 terraform-bot commented 5 minutes ago
👤 terraform-bot created PR #123
✏️  Committed by terraform-bot
```

**Setup:**

#### Step 1: Create Bot User Account
1. Create new GitHub account: `terraform-bot` (or `acme-terraform-bot`)
2. Set profile:
   - Name: "Terraform Auto-Remediation Bot"
   - Bio: "🤖 Automated Terraform fixes"
   - Avatar: Use a robot image
3. Add to your organization
4. Grant appropriate permissions

#### Step 2: Generate PAT
1. Login as bot user
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Name: `terraform-remediation-system`
5. Expiration: No expiration (or use GitHub App for auto-refresh)
6. **Scopes required:**
   - ✅ `repo` (full control of repositories)
   - ✅ `workflow` (update workflows)
   - ✅ `write:packages` (if using packages)

#### Step 3: Configure
```yaml
# k8s/deployment.yaml
GITHUB_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"
GITHUB_WEBHOOK_SECRET: "your-webhook-secret"
```

**Pros:**
- ✅ Simple setup
- ✅ Works immediately
- ✅ Easy to test locally

**Cons:**
- ⚠️ Token has broad access (security risk)
- ⚠️ Shows as regular user (less clear it's a bot)
- ⚠️ Requires managing token expiration
- ⚠️ Uses a seat in private orgs

---

## 🎨 How Commits & PRs Appear

### Commit Attribution

#### With GitHub App:
```
commit abc123def456
Author: terraform-remediation[bot] <123456+terraform-remediation[bot]@users.noreply.github.com>
Date:   Wed Mar 12 10:00:00 2024 +0000

    🔧 fix: Add missing instance_type variable
    
    Auto-generated fix for terraform validation error.
    
    Co-authored-by: Terraform Auto-Remediation Bot <bot@example.com>
```

#### With PAT:
```
commit abc123def456
Author: terraform-bot <terraform-bot@users.noreply.github.com>
Date:   Wed Mar 12 10:00:00 2024 +0000

    🔧 fix: Add missing instance_type variable
    
    Auto-generated fix for terraform validation error.
```

### PR Creation

Both methods create PRs that look like:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ terraform-remediation[bot] wants to merge 1 commit ┃
┃ from autofix/terraform-123 into main               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🤖 [AUTO-FIX] Terraform: Add missing instance_type variable

Opened by terraform-remediation[bot] • 5 minutes ago
🏷️ terraform  auto-fix  risk-low

## 🤖 Automated Terraform Fix
...
```

### Issue Creation

Issues show the creator:

```
🔥 [AUTO-FIX] Terraform workflow failed: CI

🤖 terraform-remediation[bot] opened this issue 10 minutes ago
🏷️ terraform  auto-fix  automated
```

---

## 🔒 Security Best Practices

### For Public Repositories ✅

**DO:**
1. ✅ Use GitHub App (preferred) or dedicated bot account
2. ✅ Enable "Require approval for all outside collaborators" in Actions
3. ✅ Use CODEOWNERS to require reviews for sensitive files
4. ✅ Enable branch protection rules
5. ✅ Limit bot permissions to only what's needed
6. ✅ Use secrets for tokens (never commit them!)
7. ✅ Enable audit logging
8. ✅ Set up alerts for unusual activity

**DON'T:**
1. ❌ Use personal accounts for automation
2. ❌ Use tokens with broader scope than needed
3. ❌ Store tokens in code or configs
4. ❌ Give bot admin access unless necessary
5. ❌ Forget to rotate tokens periodically

### Recommended Permissions

#### For Public Repos:
```yaml
Repository permissions:
  contents: write         # Commit code
  issues: write          # Create/update issues
  pull_requests: write   # Create PRs
  workflows: read        # Read workflow logs
  metadata: read         # Required
  
Organization permissions:
  members: read          # Read org members (optional)
```

#### For Private Repos (same as above):
Same permissions + consider:
- Team discussions access (if needed)
- Packages access (if publishing)

---

## 📋 Configuration Examples

### Example 1: GitHub App (Production)

```yaml
# k8s/deployment.yaml Secrets
apiVersion: v1
kind: Secret
metadata:
  name: terraform-healer-secrets
stringData:
  GITHUB_APP_ID: "123456"
  GITHUB_APP_PRIVATE_KEY: |
    -----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEA...
    -----END RSA PRIVATE KEY-----
  GITHUB_WEBHOOK_SECRET: "super-secret-webhook-key"
```

### Example 2: PAT with Bot User (Development)

```yaml
# k8s/deployment.yaml Secrets
apiVersion: v1
kind: Secret
metadata:
  name: terraform-healer-secrets
stringData:
  GITHUB_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"
  GITHUB_WEBHOOK_SECRET: "super-secret-webhook-key"
```

### Example 3: Local Development

```bash
# .env file (DO NOT COMMIT!)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_WEBHOOK_SECRET=your-webhook-secret
MONITORED_ORGS=your-test-org
DRY_RUN=true
```

---

## 🎭 Bot User Profile Setup

### Recommended Bot Profile:

**Username:** `terraform-remediation-bot` or `YOUR_USERNAME-terraform-bot`

**Profile:**
- **Name:** "🤖 Terraform Auto-Remediation Bot"
- **Bio:** 
  ```
  🤖 Automated Terraform failure detection and remediation
  🔧 Fixes syntax, validation, and format issues
  🛡️ 8-layer safety validation
  📚 Docs: https://github.com/YOUR_USERNAME/terraform-healer
  ```
- **Website:** Link to your documentation
- **Avatar:** Robot icon or your company logo with bot indicator
- **Email:** `terraform-bot@your-company.com` (or use noreply)

### Profile README (optional):

```markdown
# 🤖 Terraform Auto-Remediation Bot

I'm a bot that automatically fixes Terraform workflow failures!

## What I Do
- 🔍 Monitor Terraform GitHub Actions failures
- 🧠 Analyze errors using AI
- 🔧 Generate safe fixes
- 📝 Create pull requests
- 💬 Notify teams via Slack

## Safety
- 🛡️ 8-layer validation
- 🎯 Pattern-based risk detection
- ✅ No cloud credentials required
- 👥 Requires human approval for high-risk changes

## Repositories I Monitor
- YOUR_USERNAME/terraform-aws
- YOUR_USERNAME/terraform-gcp
- YOUR_USERNAME/terraform-azure

---
🤖 Powered by [Terraform Auto-Remediation System](https://github.com/YOUR_USERNAME/terraform-healer)
```

---

## 🔍 Audit Trail

### Tracking Bot Actions

All bot actions are logged and traceable:

#### In GitHub:
```
# View all PRs by bot
is:pr author:terraform-remediation[bot]

# View all issues by bot
is:issue author:terraform-remediation[bot]

# View all commits by bot
author:terraform-remediation[bot]
```

#### In Audit Logs (Enterprise):
- Organization Settings → Audit log
- Filter by: `actor:terraform-remediation[bot]`
- Export logs for compliance

#### In Your Logs:
```json
{
  "timestamp": "2024-03-12T10:00:00Z",
  "event": "pr_created",
  "repo": "org/repo",
  "pr_number": 123,
  "actor": "terraform-remediation[bot]",
  "risk_level": "low"
}
```

---

## 🚨 Security Incidents

### If Token is Compromised:

**Immediate Actions:**
1. ⚡ Revoke token immediately in GitHub
2. 🔄 Generate new token
3. 🔐 Update Kubernetes secret
4. 🔄 Restart pods: `kubectl rollout restart deployment/terraform-healer`
5. 📊 Review audit logs for suspicious activity
6. 🔔 Notify security team

**Prevention:**
- Rotate tokens every 90 days
- Use GitHub App instead (auto-managed tokens)
- Enable alerts for token usage
- Review bot actions regularly

---

## ❓ FAQ

### Q: Can I use my personal account?
**A:** ❌ No! Always use a dedicated bot account or GitHub App. Using personal accounts:
- Confuses attribution
- Creates security risks
- Violates ToS for automation
- Makes it hard to revoke access

### Q: Do I need a paid GitHub account for the bot?
**A:** 
- GitHub App: ❌ No cost for public or private repos
- PAT with bot user: ✅ Free for public repos, uses a seat in private orgs

### Q: Will the bot have access to all repos in my org?
**A:** Only repos you:
- Install the GitHub App on (for App auth)
- Give the bot user access to (for PAT auth)
- Specify in `MONITORED_REPOS` config

### Q: Can multiple people see the bot's activity?
**A:** ✅ Yes! All commits, PRs, and issues are public (if repos are public).

### Q: How do I limit bot to specific repos in public org?
**A:** Two ways:
1. Only install GitHub App on specific repos
2. Use `MONITORED_REPOS` config filter

### Q: What happens if bot creates a bad PR?
**A:** 
- Revert the PR
- Close the associated issue
- Bot actions are logged for review
- Adjust AI confidence threshold

---

## 📊 Comparison Table

| Feature | GitHub App | Personal Access Token |
|---------|-----------|----------------------|
| Shows as "[bot]" | ✅ Yes | ❌ No |
| Granular permissions | ✅ Yes | ❌ No |
| Auto-refresh tokens | ✅ Yes | ❌ No |
| Multi-org support | ✅ Easy | ⚠️ Manual |
| Setup complexity | ⚠️ Medium | ✅ Easy |
| Free for private repos | ✅ Yes | ❌ Uses seat |
| Rate limit | 🚀 5000 req/hr | ⚠️ 5000 req/hr |
| Audit trail | ✅ Clear | ⚠️ Mixed |
| Security | 🛡️ Better | ⚠️ Broader access |

---

## 🎯 Recommendation

For **public repositories**: Use **GitHub App** ✅

**Why:**
- ✅ Clearly marked as bot ([bot] suffix)
- ✅ Better security (scoped permissions)
- ✅ No seat cost
- ✅ Professional appearance
- ✅ Easier to manage at scale

**Setup time:** ~15 minutes

---

## 📚 Additional Resources

- [GitHub Apps Documentation](https://docs.github.com/en/developers/apps)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Bot Best Practices](https://docs.github.com/en/developers/overview/managing-deploy-keys)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

🤖 **Next Steps:**
1. Choose authentication method (GitHub App recommended)
2. Create and configure bot user/app
3. Update `k8s/deployment.yaml` with credentials
4. Deploy and test!

✨ Your automation will show as a professional bot user! 🚀
