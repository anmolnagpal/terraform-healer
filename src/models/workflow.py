from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk levels for terraform changes."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TerraformErrorType(str, Enum):
    """Types of Terraform errors."""
    SYNTAX = "syntax"
    VALIDATION = "validation"
    FORMAT = "format"
    PROVIDER = "provider"
    MODULE = "module"
    STATE = "state"
    UNKNOWN = "unknown"


class WorkflowFailure(BaseModel):
    """Model for a workflow failure."""
    id: Optional[int] = None
    repo_owner: str
    repo_name: str
    workflow_id: int
    workflow_run_id: int
    workflow_name: str
    job_id: Optional[int] = None
    job_name: Optional[str] = None
    branch: str
    commit_sha: str
    error_message: str
    error_type: TerraformErrorType
    log_url: str
    failed_at: datetime
    issue_number: Optional[int] = None
    pr_number: Optional[int] = None
    status: str = "detected"  # detected, analyzing, fixing, fixed, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FixAttempt(BaseModel):
    """Model for a fix attempt."""
    id: Optional[int] = None
    workflow_failure_id: int
    attempt_number: int
    fix_description: str
    changes: Dict[str, Any]  # file_path -> changes
    risk_level: RiskLevel
    confidence_score: int
    validation_passed: bool = False
    pr_number: Optional[int] = None
    pr_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ai_reasoning: Optional[str] = None
    validation_logs: Optional[str] = None


class TerraformFix(BaseModel):
    """Model for AI-generated Terraform fix."""
    files_to_change: Dict[str, str]  # file_path -> new_content
    fix_description: str
    confidence_score: int
    reasoning: str
    risk_level: RiskLevel
    patterns_detected: List[str] = []
    validation_commands: List[str] = []
