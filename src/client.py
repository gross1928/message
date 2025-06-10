import asyncio
import logging
from telethon import TelegramClient, events

from src.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_NAME
from src.db import get_all_channels
from src.processor import process_message

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the client
client = TelegramClient(TELEGRAM_SESSION_NAME, int(TELEGRAM_API_ID), TELEGRAM_API_HASH)

def get_all_subscribed_channels():
    """Fetches a unique list of all channel usernames from the database."""
    channels = get_all_channels()
    logger.info(f"Found {len(channels)} unique channels to monitor.")
    return channels

async def main():
    """The main function to run the client."""
    await client.start(phone=config.TELEGRAM_PHONE)
    logger.info("Telegram client started.")

    all_channels = get_all_subscribed_channels()

    @client.on(events.NewMessage(chats=all_channels))
    async def handler(event):
        logger.info(f"New message from {event.chat.username}. ID: {event.message.id}")
                # Trigger the full processing pipeline
        await process_message(event.chat.username, event.message)

    logger.info(f"Listening for new messages in: {', '.join(all_channels)}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # Running the client requires an asyncio event loop
    asyncio.run(main())
