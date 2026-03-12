import hmac
import hashlib
import structlog
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from src.config import settings
from src.models.github_event import GitHubWebhookEvent
from src.services.remediation_service import remediation_orchestrator

logger = structlog.get_logger()

app = FastAPI(title="Terraform Auto-Remediation System")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "terraform-healer",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Kubernetes health check."""
    return {"status": "ok"}


@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle GitHub webhook events."""
    
    # Verify webhook signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")
    
    body = await request.body()
    
    if not verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse event
    event_type = request.headers.get("X-GitHub-Event")
    payload = await request.json()
    
    logger.info("Received GitHub webhook", event_type=event_type)
    
    # Handle workflow_run events
    if event_type == "workflow_run":
        try:
            event = GitHubWebhookEvent(**payload)
            
            # Check if it's a failure and we should monitor this repo
            if event.is_failure and settings.should_monitor_repo(
                event.repo_owner, event.repo_name
            ):
                workflow_run = event.workflow_run
                
                # Process in background
                background_tasks.add_task(
                    remediation_orchestrator.handle_workflow_failure,
                    repo_owner=event.repo_owner,
                    repo_name=event.repo_name,
                    workflow_run_id=workflow_run["id"],
                    workflow_name=workflow_run["name"],
                    branch=workflow_run["head_branch"],
                    commit_sha=workflow_run["head_sha"]
                )
                
                return {"status": "processing", "run_id": workflow_run["id"]}
            else:
                return {"status": "ignored", "reason": "not a failure or not monitored"}
        
        except Exception as e:
            logger.error("Failed to process webhook", error=str(e), exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    return {"status": "ok"}


def verify_signature(payload: bytes, signature_header: str) -> bool:
    """Verify GitHub webhook signature."""
    
    if not settings.github_webhook_secret:
        logger.warning("Webhook secret not configured, skipping verification")
        return True
    
    hash_object = hmac.new(
        settings.github_webhook_secret.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    )
    
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error("Unhandled exception", error=str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
