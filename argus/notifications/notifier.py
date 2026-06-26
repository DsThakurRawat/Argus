"""
Lightweight notifier for routing alerts to external bots (Slack, Discord, Telegram).
"""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class Notifier:
    """Lightweight notifier for Slack, Discord, and Telegram."""

    async def notify(self, packet: Any, configs: dict) -> None:
        """Send notifications to enabled bots using httpx."""
        bots = configs.get("bots", {})
        if not bots:
            return

        async with httpx.AsyncClient() as client:
            if "slack" in bots:
                await self._notify_slack(client, bots["slack"], packet)
            if "discord" in bots:
                await self._notify_discord(client, bots["discord"], packet)
            if "telegram" in bots:
                await self._notify_telegram(client, bots["telegram"], packet)

    async def _notify_slack(
        self, client: httpx.AsyncClient, token_or_url: str, packet: Any
    ) -> None:
        if not token_or_url:
            logger.error("Slack notification failed: Token or URL is empty or missing.")
            return

        issue_id = (
            packet.get("issue_id")
            if isinstance(packet, dict)
            else getattr(packet, "issue_id", "N/A")
        )
        pattern = (
            packet.get("detected_pattern")
            if isinstance(packet, dict)
            else getattr(packet, "detected_pattern", "N/A")
        )
        summary = (
            packet.get("natural_language_summary")
            if isinstance(packet, dict)
            else getattr(packet, "natural_language_summary", "N/A")
        )

        payload = {
            "text": f"🚨 *Argus Alert* 🚨\n*Issue ID*: {issue_id}\n*Pattern*: {pattern}\n*Summary*: {summary}"
        }
        try:
            # Note: Slack incoming webhook URL is typically used, not bot token for simple posts.
            # If the user provides a webhook URL, it should be an http URL.
            if token_or_url.startswith("http"):
                response = await client.post(token_or_url, json=payload)
            else:
                # Fallback to chat.postMessage if they provided a token
                url = "https://slack.com/api/chat.postMessage"
                headers = {
                    "Authorization": f"Bearer {token_or_url}",
                    "Content-Type": "application/json",
                }
                payload["channel"] = "#general"
                response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Slack notification failed: {e}")

    async def _notify_discord(
        self, client: httpx.AsyncClient, webhook_url: str, packet: Any
    ) -> None:
        if not webhook_url or not webhook_url.startswith("http"):
            logger.error("Discord notification failed: Invalid or missing webhook URL.")
            return
        issue_id = (
            packet.get("issue_id")
            if isinstance(packet, dict)
            else getattr(packet, "issue_id", "N/A")
        )
        pattern = (
            packet.get("detected_pattern")
            if isinstance(packet, dict)
            else getattr(packet, "detected_pattern", "N/A")
        )
        summary = (
            packet.get("natural_language_summary")
            if isinstance(packet, dict)
            else getattr(packet, "natural_language_summary", "N/A")
        )

        payload = {
            "content": f"🚨 **Argus Alert** 🚨\n**Issue ID**: {issue_id}\n**Pattern**: {pattern}\n**Summary**: {summary}"
        }
        try:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Discord notification failed: {e}")

    async def _notify_telegram(self, client: httpx.AsyncClient, token: str, packet: Any) -> None:
        if not token:
            logger.error("Telegram notification failed: Token is empty or missing.")
            return
        if ":" in token and len(token.split(":")) >= 2:
            parts = token.split(":")
            bot_token = f"{parts[0]}:{parts[1]}"
            chat_id = parts[2] if len(parts) > 2 else "0"
        else:
            bot_token = token
            chat_id = "0"

        if chat_id == "0":
            logger.error(
                "Telegram notification failed: Chat ID is missing. Please provide the token in the format 'bot_token:chat_id'."
            )
            return

        issue_id = (
            packet.get("issue_id")
            if isinstance(packet, dict)
            else getattr(packet, "issue_id", "N/A")
        )
        pattern = (
            packet.get("detected_pattern")
            if isinstance(packet, dict)
            else getattr(packet, "detected_pattern", "N/A")
        )
        summary = (
            packet.get("natural_language_summary")
            if isinstance(packet, dict)
            else getattr(packet, "natural_language_summary", "N/A")
        )

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"🚨 Argus Alert 🚨\nIssue ID: {issue_id}\nPattern: {pattern}\nSummary: {summary}",
        }
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Telegram notification failed: {e}")


async def notify(packet: Any, configs: dict) -> None:
    """Helper function to send notifications."""
    notifier = Notifier()
    await notifier.notify(packet, configs)
