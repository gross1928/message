import logging
import openai
from telethon.tl.types import Message

from src.config import OPENAI_API_KEY
from src.db import get_or_create_channel, save_message, get_subscribers_for_channel
# We need to import the bot's application instance to send messages
from src.bot import application

# Configure OpenAI
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

logger = logging.getLogger(__name__)

def generate_summary(text: str) -> str:
    """Generates a summary for the given text using OpenAI."""
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set. Returning dummy summary.")
        return "(This is a dummy summary because the OpenAI API key is not configured.)"
    
    try:
        prompt = (
            f"Дай краткую аннотацию этого Telegram-сообщения (2–3 предложения), "
            f"выдели ключевые факты и ссылки.\n\n---\n\n{text}"
        )
        response = openai.Completion.create(
            engine="text-davinci-003", # Or another suitable model like gpt-3.5-turbo
            prompt=prompt,
            max_tokens=150,
            temperature=0.5,
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        logger.error(f"Error generating summary with OpenAI: {e}")
        return "(Could not generate a summary for this post.)"

async def process_message(channel_username: str, message: Message):
    """Processes a new message: summarizes, saves, and notifies."""
    logger.info(f"Processing message {message.id} from @{channel_username}")

    # Ensure channel exists in our DB and has its ID populated
    channel = get_or_create_channel(channel_username, message.chat_id)
    if not channel:
        logger.error(f"Could not get or create channel @{channel_username}")
        return

    # 1. Generate summary
    summary = generate_summary(message.text)
    
    # 2. Construct the original message link
    link = f"https://t.me/{channel_username}/{message.id}"

    # 3. Save to Supabase
    saved_message = save_message(channel['id'], message.id, message.text, summary, link)
    if saved_message and 'error' in saved_message and saved_message['error'] == 'already_exists':
        return # Stop processing if we've handled this message before

    # 4. Notify users
    subscribers = get_subscribers_for_channel(channel['id'])
    logger.info(f"Found {len(subscribers)} subscribers for @{channel_username}. Notifying...")
    
    notification_text = f"{summary}\n\n🔗 **Original Post**: [link]({link})"

    for telegram_id in subscribers:
        try:
            await application.bot.send_message(
                chat_id=telegram_id, 
                text=notification_text, 
                parse_mode='MarkdownV2',
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Failed to send notification to {telegram_id}: {e}")
