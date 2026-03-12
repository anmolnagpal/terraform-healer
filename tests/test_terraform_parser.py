import pytest
import asyncio
from src.services.terraform_parser import TerraformLogParser, TerraformRiskAnalyzer
from src.models.workflow import TerraformErrorType, RiskLevel


class TestTerraformLogParser:
    """Test Terraform log parsing."""
    
    def test_parse_syntax_error(self):
        """Test parsing syntax errors."""
        logs = """
Error: Invalid syntax at main.tf:10

This is a syntax error in HCL.
        """
        
        error_type, error_message, affected_files = TerraformLogParser.parse_logs(logs)
        
        assert error_type == TerraformErrorType.SYNTAX
        assert "syntax" in error_message.lower()
        assert "main.tf" in affected_files
    
    def test_parse_validation_error(self):
        """Test parsing validation errors."""
        logs = """
Error: Missing required argument

  on variables.tf line 5:
   5: variable "instance_type" {

The argument "type" is required.
        """
        
        error_type, error_message, affected_files = TerraformLogParser.parse_logs(logs)
        
        assert error_type == TerraformErrorType.VALIDATION
        assert "variables.tf" in affected_files
    
    def test_is_auto_fixable(self):
        """Test auto-fixable detection."""
        assert TerraformLogParser.is_auto_fixable(TerraformErrorType.SYNTAX)
        assert TerraformLogParser.is_auto_fixable(TerraformErrorType.FORMAT)
        assert not TerraformLogParser.is_auto_fixable(TerraformErrorType.STATE)


class TestTerraformRiskAnalyzer:
    """Test risk analysis."""
    
    def test_low_risk_format_fix(self):
        """Test low risk classification for format fixes."""
        changes = {"main.tf": "resource \"aws_instance\" \"example\" {\n  ami = \"ami-123\"\n}"}
        
        risk_level, patterns = TerraformRiskAnalyzer.analyze_changes(
            ["main.tf"],
            changes,
            ai_confidence=90
        )
        
        assert risk_level == RiskLevel.LOW
    
    def test_high_risk_iam_changes(self):
        """Test high risk classification for IAM changes."""
        changes = {
            "iam.tf": '''
resource "aws_iam_role" "example" {
  name = "example"
}
            '''
        }
        
        risk_level, patterns = TerraformRiskAnalyzer.analyze_changes(
            ["iam.tf"],
            changes,
            ai_confidence=90
        )
        
        assert risk_level == RiskLevel.HIGH
        assert len(patterns) > 0
    
    def test_critical_backend_changes(self):
        """Test critical risk for backend changes."""
        changes = {
            "backend.tf": '''
terraform {
  backend "s3" {
    bucket = "my-bucket"
  }
}
            '''
        }
        
        risk_level, patterns = TerraformRiskAnalyzer.analyze_changes(
            ["backend.tf"],
            changes,
            ai_confidence=90
        )
        
        assert risk_level == RiskLevel.CRITICAL
    
    def test_required_approvals(self):
        """Test required approvals calculation."""
        assert TerraformRiskAnalyzer.get_required_approvals(RiskLevel.LOW) == 0
        assert TerraformRiskAnalyzer.get_required_approvals(RiskLevel.MEDIUM) == 1
        assert TerraformRiskAnalyzer.get_required_approvals(RiskLevel.HIGH) == 2
        assert TerraformRiskAnalyzer.get_required_approvals(RiskLevel.CRITICAL) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
