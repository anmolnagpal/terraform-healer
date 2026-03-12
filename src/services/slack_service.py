import structlog
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.config import settings
from src.models.workflow import RiskLevel

logger = structlog.get_logger()


class SlackNotifier:
    """Send notifications to Slack."""
    
    def __init__(self):
        self.client = WebClient(token=settings.slack_bot_token)
        self.channel_id = settings.slack_channel_id
        logger.info("Slack notifier initialized", channel=self.channel_id)
    
    async def notify_pr_created(
        self,
        repo_owner: str,
        repo_name: str,
        pr_number: int,
        pr_url: str,
        title: str,
        risk_level: RiskLevel,
        fix_description: str,
        confidence_score: int
    ):
        """Notify team about new PR with emojis!"""
        
        risk_emoji = {
            RiskLevel.LOW: "🟢",
            RiskLevel.MEDIUM: "🟡",
            RiskLevel.HIGH: "🔴",
            RiskLevel.CRITICAL: "🚨"
        }
        
        risk_color = {
            RiskLevel.LOW: "good",
            RiskLevel.MEDIUM: "warning",
            RiskLevel.HIGH: "danger",
            RiskLevel.CRITICAL: "danger"
        }
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🤖 {risk_emoji.get(risk_level, '🔧')} Terraform Auto-Fix PR Created!"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*📦 Repository:*\n{repo_owner}/{repo_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*{risk_emoji.get(risk_level)} Risk Level:*\n{risk_level.value.upper()}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*🔗 PR Number:*\n#{pr_number}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*🎯 Confidence:*\n{confidence_score}%"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🔧 Fix Description:*\n{fix_description}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👀 View PR"
                        },
                        "url": pr_url,
                        "style": "primary"
                    }
                ]
            }
        ]
        
        # Add warning for high-risk PRs
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            blocks.insert(1, {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "⚠️ *HIGH RISK CHANGE* - Manual review required before merging! 🛑"
                }
            })
        
        # Add auto-merge info for low/medium risk
        if risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]:
            from src.config import settings
            blocks.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"⏰ Auto-merge in {settings.auto_merge_delay_hours}h if checks pass"
                    }
                ]
            })
        
        try:
            response = self.client.chat_postMessage(
                channel=self.channel_id,
                text=f"🤖 Terraform Auto-Fix PR Created: {title}",
                blocks=blocks,
                attachments=[{
                    "color": risk_color.get(risk_level, "warning"),
                    "text": title
                }]
            )
            
            logger.info(
                "📤 Slack notification sent",
                channel=self.channel_id,
                ts=response["ts"]
            )
            return response["ts"]
        
        except SlackApiError as e:
            logger.error("❌ Failed to send Slack notification", error=str(e))
            return None
    
    async def notify_pr_merged(
        self,
        repo_owner: str,
        repo_name: str,
        pr_number: int,
        merged_by: str
    ):
        """Notify team about PR merge with celebration!"""
        
        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=f"✅ 🎉 Terraform Auto-Fix PR #{pr_number} merged in {repo_owner}/{repo_name} by @{merged_by}! 🚀"
            )
        except SlackApiError as e:
            logger.error("❌ Failed to send merge notification", error=str(e))
    
    async def notify_fix_failed(
        self,
        repo_owner: str,
        repo_name: str,
        workflow_run_id: int,
        error_message: str
    ):
        """Notify team about fix failure."""
        
        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=f"❌ 🔥 Failed to auto-fix Terraform workflow failure in {repo_owner}/{repo_name}\n\n*Workflow Run:* {workflow_run_id}\n*Error:* {error_message[:200]}\n\n👨‍💻 Manual intervention required!"
            )
        except SlackApiError as e:
            logger.error("❌ Failed to send failure notification", error=str(e))


# Global instance
slack_notifier = SlackNotifier()
