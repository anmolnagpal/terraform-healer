from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    """Application configuration."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # GitHub Configuration
    github_app_id: Optional[str] = None
    github_app_private_key_path: Optional[str] = None
    github_webhook_secret: str
    github_token: Optional[str] = None
    
    # AI Provider
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    ai_provider: str = "anthropic"
    ai_model: str = "claude-3-5-sonnet-20241022"
    
    # Slack
    slack_bot_token: str
    slack_channel_id: str
    
    # Application
    app_env: str = "development"
    log_level: str = "INFO"
    dry_run: bool = False
    
    # Auto-Merge Settings
    auto_merge_enabled: bool = True
    auto_merge_delay_hours: int = 24
    low_risk_auto_merge: bool = True
    medium_risk_auto_merge: bool = False
    
    # Risk Detection
    max_files_changed: int = 2
    max_lines_per_file: int = 20
    ai_confidence_threshold: int = 85
    
    # Monitoring
    monitored_orgs: str = ""
    monitored_repos: str = ""
    
    # Webhook
    webhook_port: int = 8000
    webhook_host: str = "0.0.0.0"
    
    @property
    def monitored_orgs_list(self) -> List[str]:
        """Parse monitored organizations."""
        if not self.monitored_orgs:
            return []
        return [org.strip() for org in self.monitored_orgs.split(",")]
    
    @property
    def monitored_repos_list(self) -> List[str]:
        """Parse monitored repositories."""
        if not self.monitored_repos:
            return []
        return [repo.strip() for repo in self.monitored_repos.split(",")]
    
    def should_monitor_repo(self, owner: str, repo: str) -> bool:
        """Check if a repository should be monitored."""
        full_name = f"{owner}/{repo}"
        
        # If specific repos are configured, check against that list
        if self.monitored_repos_list:
            return full_name in self.monitored_repos_list
        
        # Otherwise check if org is in monitored orgs
        return owner in self.monitored_orgs_list


settings = Settings()
