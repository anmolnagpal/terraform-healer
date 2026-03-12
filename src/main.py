import sys
import structlog
from structlog.processors import JSONRenderer
import uvicorn
from src.config import settings


def setup_logging():
    """Configure structured logging."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def main():
    """Main entry point."""
    setup_logging()
    
    logger = structlog.get_logger()
    logger.info(
        "Starting Terraform Auto-Remediation System",
        env=settings.app_env,
        port=settings.webhook_port,
        monitored_orgs=settings.monitored_orgs_list
    )
    
    if settings.dry_run:
        logger.warning("DRY RUN MODE ENABLED - No actual changes will be made")
    
    # Start FastAPI server
    uvicorn.run(
        "src.api.webhook:app",
        host=settings.webhook_host,
        port=settings.webhook_port,
        log_level=settings.log_level.lower(),
        reload=settings.app_env == "development"
    )


if __name__ == "__main__":
    main()
