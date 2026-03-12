# 🤝 Contributing to Terraform Healer

First off, **thank you** for considering contributing! 🎉 **Terraform Healer** aims to make Terraform CI/CD more reliable and we need your help to make it better!

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)

## 📜 Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you're expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🚀 How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Here's how to report it:

1. **Check existing issues** - Someone might have already reported it
2. **Create a new issue** using the bug report template
3. **Include details**:
   - What you expected to happen
   - What actually happened
   - Steps to reproduce
   - Your environment (OS, Python version, Terraform version)
   - Relevant logs (sanitize sensitive data!)

### 💡 Suggesting Features

Have an idea? We'd love to hear it!

1. **Check existing issues** - It might already be planned
2. **Create a feature request** using the feature request template
3. **Explain**:
   - The problem you're trying to solve
   - Your proposed solution
   - Alternative solutions you've considered
   - Why this would benefit others

### 🔧 Contributing Code

Ready to code? Awesome!

1. **Pick an issue** - Look for `good-first-issue` or `help-wanted` labels
2. **Comment on the issue** - Let others know you're working on it
3. **Fork the repo** and create a branch
4. **Make your changes** following our coding standards
5. **Test thoroughly** - Add tests for new features
6. **Submit a PR** using the PR template

### 📝 Improving Documentation

Documentation improvements are always welcome!

- Fix typos or clarify existing docs
- Add examples or use cases
- Translate documentation (if multilingual support is added)
- Update outdated information

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Terraform 1.5+
- Git

### Local Setup

```bash
# 1. Fork and clone the repo
git clone https://github.com/YOUR_USERNAME/terraform-healer.git
cd terraform-healer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# 4. Set up pre-commit hooks
pre-commit install

# 5. Copy environment template
cp .env.example .env
# Edit .env with your test credentials

# 6. Run tests
pytest tests/ -v

# 7. Run linters
black src/ tests/
flake8 src/ tests/
isort src/ tests/
mypy src/
```

### Running Locally

```bash
# Start the service
uvicorn src.main:app --reload --port 8000

# In another terminal, send test webhook
curl -X POST http://localhost:8000/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: workflow_run" \
  -d @tests/fixtures/workflow_failure.json
```

## 🔄 Pull Request Process

### Before Submitting

- [ ] Tests pass: `pytest tests/ -v`
- [ ] Linting passes: `black . && flake8 . && isort .`
- [ ] Type checking passes: `mypy src/`
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (under "Unreleased")
- [ ] Commits follow our commit message format

### PR Guidelines

1. **Keep it focused** - One feature/fix per PR
2. **Small PRs** - Easier to review (aim for <400 lines)
3. **Write tests** - New code should have tests
4. **Update docs** - Keep documentation in sync
5. **Link issues** - Reference related issues in description
6. **Be responsive** - Address review feedback promptly

### PR Title Format

Use conventional commits format:

```
type(scope): brief description

Examples:
feat(validator): add tfsec security scanning
fix(github): handle rate limiting properly  
docs(readme): add installation instructions
test(parser): add tests for error classification
refactor(ai): simplify prompt generation
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`

### Review Process

1. **Automated checks** - CI must pass (tests, linting)
2. **Code review** - At least one maintainer approval required
3. **Testing** - Maintainers may test your changes locally
4. **Feedback** - Address review comments, push updates
5. **Merge** - Maintainer will merge once approved

## 🎨 Coding Standards

### Python Style

We follow [PEP 8](https://pep8.org/) with some tweaks:

```python
# ✅ Good
def analyze_terraform_error(
    log_content: str,
    risk_patterns: List[str],
    confidence_threshold: float = 0.85
) -> TerraformError:
    """
    Analyze Terraform error logs and classify risk level.
    
    Args:
        log_content: Raw Terraform log output
        risk_patterns: List of regex patterns to match
        confidence_threshold: Minimum confidence score (0-1)
    
    Returns:
        TerraformError with classification and metadata
    """
    # Implementation
    pass

# ❌ Bad
def analyze(log,patterns,threshold=0.85):  # No types, poor names
    # Do stuff
    return result
```

### Key Rules

- **Line length**: 120 characters max (not 79)
- **Imports**: Use `isort` (absolute imports, sorted)
- **Type hints**: Required for all functions
- **Docstrings**: Required for public functions (Google style)
- **Logging**: Use structured logging with emojis! 🎉
- **Error handling**: Specific exceptions, not bare `except:`

### Emoji Guidelines

We love emojis! Use them consistently:

- 🚀 Startup/initialization
- 🧠 AI/analysis operations
- ✅ Success/completion
- ❌ Errors/failures
- ⚠️ Warnings
- 🔍 Discovery/searching
- 🎯 Processing/working
- 📝 Logging/documentation

See [docs/EMOJI_GUIDE.md](docs/EMOJI_GUIDE.md) for full list.

### Testing Standards

```python
# ✅ Good test
def test_terraform_parser_extracts_error_message():
    """Should extract error message from Terraform plan output."""
    # Arrange
    log_content = """
    Error: Invalid resource type
    on main.tf line 42
    """
    parser = TerraformLogParser()
    
    # Act
    result = parser.extract_error(log_content)
    
    # Assert
    assert result.message == "Invalid resource type"
    assert result.file_path == "main.tf"
    assert result.line_number == 42

# ❌ Bad test
def test_stuff():
    parser = TerraformLogParser()
    result = parser.extract_error("some log")
    assert result  # What are we testing?
```

## 💬 Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format
type(scope): subject

[optional body]

[optional footer]

# Examples
feat(slack): add support for Slack threads
fix(webhook): handle missing X-GitHub-Event header
docs(contributing): add commit message guidelines
test(validator): add tests for risk classification
refactor(ai): extract prompt templates to separate file

# Breaking changes
feat(api)!: change webhook endpoint path

BREAKING CHANGE: Webhook endpoint moved from /webhook to /api/v1/webhook
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding/updating tests
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `chore`: Maintenance (dependencies, build config)
- `ci`: CI/CD changes
- `style`: Code style only (formatting, no logic change)

## 🏷️ Issue Labels

We use labels to organize issues:

- `bug` 🐛 - Something isn't working
- `feature` ✨ - New feature request
- `documentation` 📝 - Documentation improvements
- `good-first-issue` 🎓 - Good for newcomers
- `help-wanted` 🆘 - Extra attention needed
- `priority-high` 🔥 - Critical issue
- `priority-low` 🧊 - Nice to have
- `wontfix` 🚫 - This won't be worked on
- `duplicate` 👥 - This issue already exists
- `enhancement` 🚀 - Improvement to existing feature
- `question` ❓ - Further information requested

## 🎓 Good First Issues

New to the project? Look for issues labeled `good-first-issue`:

- Documentation improvements
- Adding tests
- Fixing typos
- Small bug fixes
- Adding examples

## 📞 Getting Help

Need help?

- 💬 **[GitHub Discussions](https://github.com/YOUR_USERNAME/terraform-healer/discussions)** - Ask questions, share ideas
- 🐛 **[GitHub Issues](https://github.com/YOUR_USERNAME/terraform-healer/issues)** - Report bugs, request features
- 📧 **Email maintainers** - For sensitive issues

## 🙏 Recognition

Contributors are recognized in:

- README.md contributors section
- CHANGELOG.md for each release
- GitHub's contributor graph

## 📚 Resources

- [Python Best Practices](https://docs.python-guide.org/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub API Documentation](https://docs.github.com/en/rest)

## ❤️ Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute! 🎉

---

**Questions?** Open a discussion or issue - we're here to help! 🚀
