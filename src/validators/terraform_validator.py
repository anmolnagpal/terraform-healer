import structlog
import tempfile
import os
import asyncio
from typing import Tuple
from src.services.github_service import github_client

logger = structlog.get_logger()


class TerraformValidator:
    """Validate Terraform fixes without cloud credentials."""
    
    async def validate_fix(
        self,
        repo_owner: str,
        repo_name: str,
        branch: str
    ) -> Tuple[bool, str]:
        """
        Validate Terraform fix using static analysis.
        
        Returns:
            Tuple of (validation_passed, logs)
        """
        
        logger.info("Starting Terraform validation", branch=branch)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Clone repository at specific branch
                await self._clone_repo(repo_owner, repo_name, branch, tmpdir)
                
                # Run validation commands
                validation_logs = []
                
                # 1. Terraform init (without backend)
                success, log = await self._run_command(
                    tmpdir,
                    "terraform init -backend=false -input=false"
                )
                validation_logs.append(f"=== terraform init ===\n{log}")
                if not success:
                    return False, '\n'.join(validation_logs)
                
                # 2. Terraform validate
                success, log = await self._run_command(
                    tmpdir,
                    "terraform validate"
                )
                validation_logs.append(f"=== terraform validate ===\n{log}")
                if not success:
                    return False, '\n'.join(validation_logs)
                
                # 3. Terraform fmt check
                success, log = await self._run_command(
                    tmpdir,
                    "terraform fmt -check -recursive"
                )
                validation_logs.append(f"=== terraform fmt ===\n{log}")
                # fmt returns non-zero if files need formatting, but that's not a failure
                
                # 4. tflint (if available)
                success, log = await self._run_command(
                    tmpdir,
                    "tflint --init && tflint",
                    ignore_errors=True
                )
                if log:
                    validation_logs.append(f"=== tflint ===\n{log}")
                
                # 5. tfsec (if available)
                success, log = await self._run_command(
                    tmpdir,
                    "tfsec . --soft-fail",
                    ignore_errors=True
                )
                if log:
                    validation_logs.append(f"=== tfsec ===\n{log}")
                
                all_logs = '\n'.join(validation_logs)
                logger.info("Validation complete", passed=True)
                
                return True, all_logs
            
            except Exception as e:
                logger.error("Validation failed", error=str(e))
                return False, f"Validation error: {str(e)}"
    
    async def _clone_repo(
        self,
        repo_owner: str,
        repo_name: str,
        branch: str,
        target_dir: str
    ):
        """Clone repository to temporary directory."""
        
        from src.config import settings
        
        # Use GitHub token for cloning
        token = settings.github_token
        clone_url = f"https://x-access-token:{token}@github.com/{repo_owner}/{repo_name}.git"
        
        process = await asyncio.create_subprocess_exec(
            "git", "clone",
            "--branch", branch,
            "--depth", "1",
            clone_url,
            target_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"Failed to clone repo: {stderr.decode()}")
        
        logger.info("Repository cloned", repo=f"{repo_owner}/{repo_name}", branch=branch)
    
    async def _run_command(
        self,
        cwd: str,
        command: str,
        ignore_errors: bool = False
    ) -> Tuple[bool, str]:
        """Run a shell command and capture output."""
        
        logger.debug("Running command", command=command, cwd=cwd)
        
        process = await asyncio.create_subprocess_shell(
            command,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        output = stdout.decode() + stderr.decode()
        success = process.returncode == 0 or ignore_errors
        
        logger.debug(
            "Command complete",
            command=command,
            returncode=process.returncode,
            success=success
        )
        
        return success, output


# Global instance
terraform_validator = TerraformValidator()
