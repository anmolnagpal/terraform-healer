import structlog
from typing import Optional
from anthropic import Anthropic
from openai import OpenAI
from src.config import settings
from src.models.workflow import TerraformFix, RiskLevel, TerraformErrorType

logger = structlog.get_logger()


class AIFixGenerator:
    """Generate Terraform fixes using AI."""
    
    def __init__(self):
        self.provider = settings.ai_provider
        
        if self.provider == "anthropic":
            self.client = Anthropic(api_key=settings.anthropic_api_key)
        elif self.provider == "openai":
            self.client = OpenAI(api_key=settings.openai_api_key)
        else:
            raise ValueError(f"Unknown AI provider: {self.provider}")
        
        logger.info("AI Fix Generator initialized", provider=self.provider)
    
    async def generate_fix(
        self,
        error_type: TerraformErrorType,
        error_message: str,
        affected_files: list,
        repo_owner: str,
        repo_name: str,
        commit_sha: str
    ) -> Optional[TerraformFix]:
        """Generate a fix for the Terraform error."""
        
        # Fetch affected file contents
        from src.services.github_service import github_client
        
        file_contents = {}
        for file_path in affected_files[:3]:  # Limit to 3 files
            content, _ = github_client.get_file_content(
                repo_owner, repo_name, file_path, ref=commit_sha
            )
            if content:
                file_contents[file_path] = content
        
        if not file_contents:
            logger.warning("No file contents available for fix generation")
            return None
        
        # Generate fix using AI
        prompt = self._build_prompt(error_type, error_message, file_contents)
        
        try:
            if self.provider == "anthropic":
                response = await self._call_anthropic(prompt)
            else:
                response = await self._call_openai(prompt)
            
            # Parse AI response into TerraformFix
            fix = self._parse_ai_response(response)
            return fix
        
        except Exception as e:
            logger.error("Failed to generate fix", error=str(e))
            return None
    
    def _build_prompt(
        self,
        error_type: TerraformErrorType,
        error_message: str,
        file_contents: dict
    ) -> str:
        """Build prompt for AI fix generation."""
        
        prompt = f"""You are a Terraform expert. A Terraform workflow has failed with the following error:

ERROR TYPE: {error_type.value}

ERROR MESSAGE:
{error_message}

AFFECTED FILES AND THEIR CURRENT CONTENT:
"""
        
        for file_path, content in file_contents.items():
            prompt += f"\n--- {file_path} ---\n{content}\n"
        
        prompt += """

YOUR TASK:
1. Analyze the error and identify the root cause
2. Generate a minimal fix that addresses ONLY this specific error
3. Do NOT refactor, reorganize, or add new resources
4. Maintain existing resource names and attributes
5. Ensure HCL syntax is valid

IMPORTANT CONSTRAINTS:
- Change maximum 20 lines per file
- Change maximum 2 files total
- Do NOT modify: resource names, outputs, provisioners, lifecycle blocks
- Do NOT add force_destroy = true
- Do NOT disable prevent_destroy
- Do NOT change backend configuration

RESPOND IN JSON FORMAT:
{
  "files_to_change": {
    "path/to/file.tf": "FULL NEW CONTENT OF FILE"
  },
  "fix_description": "Brief description of what was fixed",
  "confidence_score": 0-100,
  "reasoning": "Why this fix addresses the error",
  "patterns_detected": ["list of any risky patterns you see"]
}

If the error cannot be safely auto-fixed, set confidence_score to 0 and explain why in reasoning.
"""
        
        return prompt
    
    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API."""
        message = self.client.messages.create(
            model=settings.ai_model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        response = self.client.chat.completions.create(
            model=settings.ai_model,
            messages=[
                {"role": "system", "content": "You are a Terraform expert that generates minimal, safe fixes."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    
    def _parse_ai_response(self, response: str) -> TerraformFix:
        """Parse AI response into TerraformFix object."""
        import json
        
        # Extract JSON from response (handle markdown code blocks)
        json_str = response
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0].strip()
        
        data = json.loads(json_str)
        
        # Determine risk level based on patterns
        risk_level = RiskLevel.LOW
        if data.get("patterns_detected"):
            # Simple heuristic - can be improved
            if any("iam_" in p.lower() or "security" in p.lower() for p in data["patterns_detected"]):
                risk_level = RiskLevel.HIGH
            elif len(data["patterns_detected"]) > 0:
                risk_level = RiskLevel.MEDIUM
        
        return TerraformFix(
            files_to_change=data["files_to_change"],
            fix_description=data["fix_description"],
            confidence_score=data["confidence_score"],
            reasoning=data["reasoning"],
            risk_level=risk_level,
            patterns_detected=data.get("patterns_detected", []),
            validation_commands=[
                "terraform init -backend=false",
                "terraform validate",
                "terraform fmt -check"
            ]
        )


# Global instance
ai_fix_generator = AIFixGenerator()
