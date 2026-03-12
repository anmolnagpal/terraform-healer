<div align="center">

# 🏥 Terraform Healer

**AI-powered Terraform failure remediation. Heal your pipelines automatically.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Terraform 1.5+](https://img.shields.io/badge/terraform-1.5+-purple.svg)](https://www.terraform.io/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-ready-brightgreen.svg)](https://kubernetes.io/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

**Terraform Healer** is an intelligent Kubernetes-deployed system that automatically detects, analyzes, and fixes Terraform workflow failures using AI. When your Terraform CI/CD pipeline fails, Terraform Healer springs into action—analyzing the error, generating a fix, validating it through 8 safety layers, and creating a pull request for review. 

**Stop debugging Terraform manually. Let AI heal your infrastructure! 🏥✨**

## 🎯 Features

- **Automatic Detection**: Real-time monitoring of Terraform GitHub Actions workflows via webhooks
- **AI-Powered Fixes**: Uses Claude/OpenAI to generate intelligent, context-aware fixes
- **Multi-Layered Safety**: 8 layers of validation and risk analysis
- **Smart PR Creation**: Automatically creates PRs with detailed context and risk assessment
- **Slack Integration**: Team notifications for all PR activities
- **Auto-Merge**: Configurable auto-merge based on risk level and time delay
- **Multi-Org Support**: Monitor multiple GitHub organizations and repositories

## 🛡️ Safety Guardrails

### Risk Levels
- **LOW** (🟢): Format/syntax fixes, <10 lines, 24h auto-merge
- **MEDIUM** (🟡): Variable updates, 10-20 lines, requires 1 approval
- **HIGH** (🔴): IAM/security patterns, >20 lines, requires 2+ approvals
- **CRITICAL** (🚨): Production/state changes, requires 3+ approvals

### Validation Pipeline
1. `terraform init -backend=false`
2. `terraform validate`
3. `terraform fmt -check`
4. `tflint` (best practices)
5. `tfsec` (security scanning)
6. Pattern-based risk detection
7. AI multi-agent validation

### Auto-Fixable Issues
✅ Syntax errors
✅ Format issues (`terraform fmt`)
✅ Validation errors (missing arguments)
✅ Deprecated syntax

### Never Auto-Fixed
❌ IAM/security changes (flagged as HIGH risk)
❌ Resource destruction
❌ State file issues
❌ Backend configuration

## ⚡ Why Terraform Healer?

- 🤖 **Fully Automated** - No manual intervention for common failures
- 🛡️ **Production Safe** - 8 layers of validation before any change
- 🎯 **Terraform-First** - Built specifically for Terraform, not generic CI/CD
- 🚫 **No Cloud Credentials** - Pattern-based validation without cloud access
- 🌐 **Multi-Org Ready** - Monitor multiple GitHub organizations
- 💬 **Team Friendly** - Rich Slack notifications with emojis
- 📊 **Risk-Aware** - Smart classification (LOW/MEDIUM/HIGH/CRITICAL)

## 🚀 Quick Start

### Prerequisites
- Kubernetes cluster
- GitHub Personal Access Token or GitHub App
- Anthropic API key or OpenAI API key
- Slack Bot Token (optional)

### 1. Build and Push Docker Image

```bash
./build.sh v1.0.0
docker push your-registry/terraform-auto-remediation:v1.0.0
```

### 2. Configure and Deploy

```bash
# Edit k8s/deployment.yaml with your values
vim k8s/deployment.yaml

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
```

### 3. Configure GitHub Webhook

1. Go to your GitHub organization settings → Webhooks → Add webhook
2. Payload URL: `https://tf-remediation.your-domain.com/webhook/github`
3. Content type: `application/json`
4. Secret: Your `GITHUB_WEBHOOK_SECRET`
5. Events: Select "Workflow runs"

## 🔧 How It Works

```
GitHub Actions Failure
   ↓
Webhook Received
   ↓
Fetch & Parse Logs
   ↓
AI Generate Fix (3-agent validation)
   ↓
Risk Analysis (pattern-based)
   ↓
Create Branch & Apply Fix
   ↓
Validate (terraform validate, fmt, tfsec)
   ↓
Create GitHub Issue
   ↓
Create Pull Request
   ↓
Notify Slack
   ↓
Auto-merge after 24h (if LOW/MEDIUM risk)
```

## 📊 Configuration

See `.env.example` for all configuration options.

Key settings:
- `MONITORED_ORGS`: GitHub orgs to monitor
- `AI_CONFIDENCE_THRESHOLD`: Minimum confidence (default: 85)
- `AUTO_MERGE_DELAY_HOURS`: Hours before auto-merge (default: 24)

## 🔒 Security

- HMAC webhook signature verification
- No cloud credentials required for validation
- Non-root container (UID 1000)
- Pattern-based risk detection
- Multi-layer validation

## 🤖 Bot User Configuration

The system needs GitHub credentials to commit code and create PRs. You have two options:

### Option 1: GitHub App (Recommended) ✅
- Shows as `terraform-remediation[bot]` in commits and PRs
- Clear bot attribution
- Better security with granular permissions
- See [Authentication Guide](./docs/GITHUB_AUTHENTICATION.md)

### Option 2: Personal Access Token 🔑
- Use a dedicated bot account (e.g., `@terraform-bot`)
- Shows as that user in commits
- Simpler setup but broader permissions
- See [Authentication Guide](./docs/GITHUB_AUTHENTICATION.md)

**Important for Public Repos:**
- ✅ DO use GitHub App or dedicated bot account
- ❌ DON'T use personal accounts for automation
- See full guide: [docs/GITHUB_AUTHENTICATION.md](./docs/GITHUB_AUTHENTICATION.md)

## 🤝 Contributing

We welcome contributions! Please see:

- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community standards
- [Security Policy](SECURITY.md) - Reporting vulnerabilities
- [Development Setup](CONTRIBUTING.md#development-setup) - Get started locally

Looking for your first contribution? Check out issues labeled [`good-first-issue`](https://github.com/anmolnagpal/terraform-healer/labels/good-first-issue)! 🎓

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Terraform](https://www.terraform.io/) - Infrastructure as Code
- [Anthropic Claude](https://www.anthropic.com/) - AI-powered fix generation
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [PyGithub](https://pygithub.readthedocs.io/) - GitHub API client

## 🌟 Star History

If this project helped you, please consider giving it a ⭐ on GitHub!

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/anmolnagpal/terraform-healer/issues/new?template=bug_report.md)
- ✨ **Feature Requests**: [Open an issue](https://github.com/anmolnagpal/terraform-healer/issues/new?template=feature_request.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/anmolnagpal/terraform-healer/discussions)
- 📚 **Documentation**: [docs/](./docs/)

---

<div align="center">

⚠️ **Always review auto-generated PRs before merging production infrastructure!**

Made with ❤️ by the open source community

**Star ⭐ this repo if Terraform Healer helped you!**

[⬆ Back to Top](#-terraform-healer)

</div>

