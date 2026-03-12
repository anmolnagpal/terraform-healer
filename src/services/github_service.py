import structlog
from typing import Optional
from github import Github, GithubIntegration
from src.config import settings

logger = structlog.get_logger()


class GitHubClient:
    """
    GitHub API client wrapper.
    
    Supports two authentication methods:
    1. GitHub App (recommended) - Shows as 'bot-name[bot]' in commits/PRs
    2. Personal Access Token - Shows as the token owner's username
    
    For public repositories, GitHub App is recommended for:
    - Clear bot attribution
    - Granular permissions
    - Better security
    - Professional appearance
    """
    
    def __init__(self):
        self._client: Optional[Github] = None
        self._setup_client()
    
    def _setup_client(self):
        """Initialize GitHub client with appropriate authentication."""
        if settings.github_token:
            # Method 2: Personal Access Token
            # Commits will show as the token owner (e.g., @terraform-bot)
            self._client = Github(settings.github_token)
            logger.info(
                "🔑 GitHub client initialized with Personal Access Token",
                auth_method="token"
            )
        elif settings.github_app_id and settings.github_app_private_key_path:
            # Method 1: GitHub App (recommended)
            # Commits will show as 'app-name[bot]' (e.g., terraform-remediation[bot])
            with open(settings.github_app_private_key_path, 'r') as key_file:
                private_key = key_file.read()
            
            integration = GithubIntegration(
                settings.github_app_id,
                private_key
            )
            # Get installation for first org (can be improved)
            installations = integration.get_installations()
            installation = list(installations)[0]
            self._client = integration.get_github_for_installation(installation.id)
            logger.info(
                "🤖 GitHub client initialized with GitHub App",
                app_id=settings.github_app_id,
                auth_method="app"
            )
        else:
            raise ValueError(
                "❌ No GitHub authentication configured! "
                "Provide either GITHUB_TOKEN or GITHUB_APP_ID + GITHUB_APP_PRIVATE_KEY_PATH. "
                "See docs/GITHUB_AUTHENTICATION.md for setup instructions."
            )
    
    @property
    def client(self) -> Github:
        """Get GitHub client instance."""
        if not self._client:
            self._setup_client()
        return self._client
    
    def get_repo(self, owner: str, repo: str):
        """Get repository object."""
        return self.client.get_repo(f"{owner}/{repo}")
    
    def get_workflow_run(self, owner: str, repo: str, run_id: int):
        """Get workflow run."""
        repo = self.get_repo(owner, repo)
        return repo.get_workflow_run(run_id)
    
    def get_workflow_job(self, owner: str, repo: str, job_id: int):
        """Get workflow job."""
        repo = self.get_repo(owner, repo)
        # PyGithub doesn't have direct job access, use API
        return self.client.get_repo(f"{owner}/{repo}").get_workflow_job(job_id)
    
    async def get_workflow_logs(self, owner: str, repo: str, run_id: int) -> str:
        """Fetch workflow logs."""
        try:
            workflow_run = self.get_workflow_run(owner, repo, run_id)
            # Get logs URL
            logs_url = workflow_run.logs_url
            
            # Download logs
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    logs_url,
                    headers={"Authorization": f"token {settings.github_token}"},
                    follow_redirects=True
                )
                response.raise_for_status()
                return response.text
        except Exception as e:
            logger.error("Failed to fetch workflow logs", error=str(e))
            raise
    
    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: list = None
    ):
        """Create a GitHub issue."""
        repo_obj = self.get_repo(owner, repo)
        return repo_obj.create_issue(
            title=title,
            body=body,
            labels=labels or []
        )
    
    def update_issue(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        body: str = None,
        state: str = None
    ):
        """Update a GitHub issue."""
        repo_obj = self.get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        if body:
            issue.edit(body=body)
        if state:
            issue.edit(state=state)
        
        return issue
    
    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str,
        labels: list = None
    ):
        """Create a pull request."""
        repo_obj = self.get_repo(owner, repo)
        pr = repo_obj.create_pull(
            title=title,
            body=body,
            head=head,
            base=base
        )
        
        if labels:
            pr.add_to_labels(*labels)
        
        return pr
    
    def create_branch(self, owner: str, repo: str, branch_name: str, from_sha: str):
        """Create a new branch."""
        repo_obj = self.get_repo(owner, repo)
        ref = f"refs/heads/{branch_name}"
        return repo_obj.create_git_ref(ref=ref, sha=from_sha)
    
    def update_file(
        self,
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str,
        sha: str = None
    ):
        """
        Update or create a file in the repository.
        
        The commit will be attributed to:
        - GitHub App: Shows as 'app-name[bot]' (e.g., terraform-remediation[bot])
        - PAT: Shows as the token owner (e.g., @terraform-bot)
        """
        repo_obj = self.get_repo(owner, repo)
        
        if sha:
            # Update existing file
            return repo_obj.update_file(
                path=path,
                message=message,
                content=content,
                sha=sha,
                branch=branch
            )
        else:
            # Create new file
            return repo_obj.create_file(
                path=path,
                message=message,
                content=content,
                branch=branch
            )
    
    def get_file_content(self, owner: str, repo: str, path: str, ref: str = None):
        """Get file content from repository."""
        repo_obj = self.get_repo(owner, repo)
        try:
            file_content = repo_obj.get_contents(path, ref=ref)
            return file_content.decoded_content.decode('utf-8'), file_content.sha
        except Exception:
            return None, None


# Global instance
github_client = GitHubClient()
