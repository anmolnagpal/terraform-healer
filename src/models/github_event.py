from typing import Optional, Dict, Any
from pydantic import BaseModel


class GitHubWebhookEvent(BaseModel):
    """Model for GitHub webhook events."""
    action: str
    workflow_run: Optional[Dict[str, Any]] = None
    workflow_job: Optional[Dict[str, Any]] = None
    repository: Dict[str, Any]
    sender: Dict[str, Any]
    organization: Optional[Dict[str, Any]] = None
    
    @property
    def repo_full_name(self) -> str:
        """Get full repository name."""
        return self.repository.get("full_name", "")
    
    @property
    def repo_owner(self) -> str:
        """Get repository owner."""
        return self.repository.get("owner", {}).get("login", "")
    
    @property
    def repo_name(self) -> str:
        """Get repository name."""
        return self.repository.get("name", "")
    
    @property
    def is_workflow_run_event(self) -> bool:
        """Check if this is a workflow_run event."""
        return self.workflow_run is not None
    
    @property
    def is_workflow_job_event(self) -> bool:
        """Check if this is a workflow_job event."""
        return self.workflow_job is not None
    
    @property
    def is_failure(self) -> bool:
        """Check if the workflow/job failed."""
        if self.workflow_run:
            return self.workflow_run.get("conclusion") == "failure"
        if self.workflow_job:
            return self.workflow_job.get("conclusion") == "failure"
        return False
