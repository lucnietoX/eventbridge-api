"""Service for handling Notion payments."""

from asyncio.log import logger
import os
import requests


async def create_notion_payment(
    event_id: str,
    event_type: str,
    status: str,
    customer_email: str,
    amount: float,
    currency: str,
) -> bool:
    """
    Create a payment entry in Notion for the given page ID with the specified amount and currency.
    """
    notion_api_url = os.getenv("NOTION_API_URL")
    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_database_id = os.getenv("NOTION_DATABASE_ID")

    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    logger.info("Creating Notion payment entry for Event ID: %s", event_id)

    data = {
        "parent": {"database_id": notion_database_id},
        "properties": {
            "EventId": {"title": [{"text": {"content": str(event_id)}}]},
            "EventType": {"rich_text": [{"text": {"content": str(event_type)}}]},
            "Source": {"rich_text": [{"text": {"content": "stripe"}}]},
            "Status": {"rich_text": [{"text": {"content": str(status)}}]},
            "CustomerEmail": {"email": str(customer_email)},
            "Currency": {"rich_text": [{"text": {"content": str(currency)}}]},
            "Amount": {"number": float(amount)},
        },
    }

    try:
        logger.info("Sending request to Notion API for Event ID: %s", event_id)
        logger.info("Notion API request data: %s", data)
        response = requests.post(notion_api_url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException:
        logger.error("Failed to create Notion payment entry for Event ID: %s", event_id)
        logger.error(
            "Notion API response: %s",
            response.text if "response" in locals() else "No response",
        )
        return False
