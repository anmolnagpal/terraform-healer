import re
import structlog
from typing import Dict, List, Tuple, Optional
from src.models.workflow import TerraformErrorType, RiskLevel

logger = structlog.get_logger()


class TerraformLogParser:
    """Parse Terraform workflow logs and extract error information."""
    
    # Terraform error patterns
    ERROR_PATTERNS = {
        TerraformErrorType.SYNTAX: [
            r"Error: Invalid.*syntax",
            r"Error: Argument or block definition required",
            r"Error: Unsupported block type",
            r"Error: Missing.*name",
        ],
        TerraformErrorType.VALIDATION: [
            r"Error: Missing required argument",
            r"Error: Invalid.*value",
            r"Error: Reference to undeclared",
            r"Error: Unsupported attribute",
        ],
        TerraformErrorType.FORMAT: [
            r"terraform fmt.*failed",
            r"formatting.*error",
        ],
        TerraformErrorType.PROVIDER: [
            r"Error: Failed to query available provider packages",
            r"Error: Incompatible provider version",
            r"Error: Provider.*not found",
        ],
        TerraformErrorType.MODULE: [
            r"Error: Module not installed",
            r"Error: Failed to load.*module",
            r"Error: Incompatible module version",
        ],
        TerraformErrorType.STATE: [
            r"Error: Failed to get existing.*state",
            r"Error: Error acquiring the state lock",
            r"Error: Backend initialization required",
        ],
    }
    
    # Patterns that indicate workflow-level issues (not Terraform code issues)
    WORKFLOW_ISSUE_PATTERNS = [
        r"Invalid workflow file",
        r"Workflow syntax error",
        r"Unknown job",
        r"Unable to resolve action",
        r"Action .* not found",
    ]
    
    @staticmethod
    def parse_logs(logs: str) -> Tuple[TerraformErrorType, str, List[str]]:
        """
        Parse Terraform logs and extract error information.
        
        Works with both direct workflows and reusable workflows from 3rd party orgs.
        The logs contain Terraform output regardless of where the workflow is defined.
        
        Returns:
            Tuple of (error_type, error_message, affected_files)
        """
        error_type = TerraformErrorType.UNKNOWN
        error_message = ""
        affected_files = []
        
        # Check if this is a workflow-level issue (not Terraform code issue)
        for pattern in TerraformLogParser.WORKFLOW_ISSUE_PATTERNS:
            if re.search(pattern, logs, re.IGNORECASE):
                logger.warning("Detected workflow-level issue, not Terraform code issue")
                return TerraformErrorType.UNKNOWN, logs[:500], []
        
        # Find error messages
        error_lines = []
        for line in logs.split('\n'):
            if 'Error:' in line or 'error' in line.lower():
                error_lines.append(line.strip())
        
        if error_lines:
            error_message = '\n'.join(error_lines[:10])  # First 10 error lines
        
        # Classify error type
        for err_type, patterns in TerraformLogParser.ERROR_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, logs, re.IGNORECASE):
                    error_type = err_type
                    break
            if error_type != TerraformErrorType.UNKNOWN:
                break
        
        # Extract affected files
        file_pattern = r'on ([^\s]+\.tf(?:vars)?)'
        file_matches = re.findall(file_pattern, logs)
        affected_files = list(set(file_matches))
        
        logger.info(
            "Parsed Terraform logs",
            error_type=error_type.value,
            files_affected=len(affected_files)
        )
        
        return error_type, error_message, affected_files
    
    @staticmethod
    def is_auto_fixable(error_type: TerraformErrorType) -> bool:
        """Determine if error type is auto-fixable."""
        fixable_types = {
            TerraformErrorType.SYNTAX,
            TerraformErrorType.VALIDATION,
            TerraformErrorType.FORMAT,
        }
        return error_type in fixable_types


class TerraformRiskAnalyzer:
    """Analyze Terraform changes for risk level."""
    
    # High-risk patterns in Terraform code
    HIGH_RISK_PATTERNS = [
        # IAM and Permissions
        r'resource\s+"aws_iam_',
        r'resource\s+"azurerm_role_',
        r'resource\s+"google_project_iam_',
        r'resource\s+"google_service_account_',
        
        # Security Groups and Firewalls
        r'resource\s+"aws_security_group',
        r'resource\s+"azurerm_network_security_',
        r'resource\s+"google_compute_firewall',
        
        # Network Configuration
        r'resource\s+"aws_vpc',
        r'resource\s+"azurerm_virtual_network',
        r'resource\s+"google_compute_network',
        
        # Destruction Flags
        r'force_destroy\s*=\s*true',
        r'prevent_destroy\s*=\s*false',
        r'lifecycle\s*{\s*prevent_destroy',
        
        # Provisioners (can execute arbitrary code)
        r'provisioner\s+"',
    ]
    
    MEDIUM_RISK_PATTERNS = [
        # Module changes
        r'module\s+"',
        r'source\s*=',
        
        # Output changes
        r'output\s+"',
        
        # Variables
        r'variable\s+"',
    ]
    
    CRITICAL_PATTERNS = [
        # State/Backend
        r'terraform\s*{\s*backend',
        r'backend\s+"',
        
        # Production indicators
        r'prod',
        r'production',
    ]
    
    @staticmethod
    def analyze_changes(
        files_changed: List[str],
        changes: Dict[str, str],
        ai_confidence: int
    ) -> Tuple[RiskLevel, List[str]]:
        """
        Analyze changes and determine risk level.
        
        Returns:
            Tuple of (risk_level, patterns_detected)
        """
        patterns_detected = []
        
        # Combine all changes for analysis
        all_changes = '\n'.join(changes.values())
        
        # Check for critical patterns
        for pattern in TerraformRiskAnalyzer.CRITICAL_PATTERNS:
            if re.search(pattern, all_changes, re.IGNORECASE):
                patterns_detected.append(f"CRITICAL: {pattern}")
        
        if patterns_detected:
            return RiskLevel.CRITICAL, patterns_detected
        
        # Check for high-risk patterns
        for pattern in TerraformRiskAnalyzer.HIGH_RISK_PATTERNS:
            if re.search(pattern, all_changes, re.IGNORECASE):
                patterns_detected.append(f"HIGH: {pattern}")
        
        if patterns_detected:
            return RiskLevel.HIGH, patterns_detected
        
        # Check for medium-risk patterns
        for pattern in TerraformRiskAnalyzer.MEDIUM_RISK_PATTERNS:
            if re.search(pattern, all_changes, re.IGNORECASE):
                patterns_detected.append(f"MEDIUM: {pattern}")
        
        # Check change metrics
        num_files = len(files_changed)
        total_lines = sum(len(content.split('\n')) for content in changes.values())
        
        # Risk based on metrics
        if patterns_detected or num_files > 1 or total_lines > 20:
            return RiskLevel.MEDIUM, patterns_detected
        
        # Low confidence = higher risk
        if ai_confidence < 85:
            return RiskLevel.MEDIUM, ["Low AI confidence"]
        
        return RiskLevel.LOW, patterns_detected
    
    @staticmethod
    def get_required_approvals(risk_level: RiskLevel) -> int:
        """Get required number of approvals based on risk."""
        return {
            RiskLevel.LOW: 0,
            RiskLevel.MEDIUM: 1,
            RiskLevel.HIGH: 2,
            RiskLevel.CRITICAL: 3,
        }.get(risk_level, 2)
    
    @staticmethod
    def can_auto_merge(risk_level: RiskLevel) -> bool:
        """Check if auto-merge is allowed for this risk level."""
        from src.config import settings
        
        if risk_level == RiskLevel.LOW:
            return settings.low_risk_auto_merge
        elif risk_level == RiskLevel.MEDIUM:
            return settings.medium_risk_auto_merge
        else:
            return False
