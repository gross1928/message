import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
)

from src.config import TELEGRAM_BOT_TOKEN
from src.db import (
    get_or_create_user, add_subscription, get_subscriptions, remove_all_subscriptions
)

# States for conversation
CHANNEL_INPUT = 0

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks for a channel."""
    user = update.effective_user
    get_or_create_user(user.id, user.username)
    
    await update.message.reply_text(
        f"Hi {user.first_name}! Отправь мне юзернейм (например, @durov) или ссылку на публичный канал, \n"
        f"на который хочешь подписаться. \n\n"
        f"Чтобы закончить, отправь /done."
    )
    
    return CHANNEL_INPUT


async def list_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all current subscriptions for the user."""
    user_id = update.effective_user.id
    subscriptions = get_subscriptions(user_id)
    if not subscriptions:
        await update.message.reply_text("You are not subscribed to any channels yet.")
        return

    message = "Your current subscriptions:\n"
    # Using a simple join for Markdown compatibility
    subs_text = "\n".join([f"- @{sub}" for sub in subscriptions])
    await update.message.reply_text(message + subs_text)


async def handle_channel_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the channel input from the user."""
    user_id = update.effective_user.id
    text = update.message.text
    
    # Extract username from URL or direct mention
    if '/' in text:
        channel_username = text.split('/')[-1]
    else:
        channel_username = text.lstrip('@')

    result = add_subscription(user_id, channel_username)

    if result and 'error' in result and result['error'] == 'already_subscribed':
        await update.message.reply_text(f"Вы уже подписаны на @{channel_username}. Присылайте следующий или нажмите /done.")
    elif result:
        await update.message.reply_text(f"Отлично! Канал @{channel_username} добавлен. Присылайте следующий или нажмите /done.")
    else:
        await update.message.reply_text(f"Не удалось добавить @{channel_username}. Убедитесь, что это правильный юзернейм публичного канала.")

    return CHANNEL_INPUT

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ends the conversation."""
    await update.message.reply_text("Отлично! Я начну мониторить новые посты в добавленных каналах.")
    return ConversationHandler.END


async def unsubscribe_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unsubscribes the user from all channels."""
    user_id = update.effective_user.id
    success = remove_all_subscriptions(user_id)

    if success:
        await update.message.reply_text("You have been unsubscribed from all channels.")
    else:
        await update.message.reply_text("An error occurred, or you had no subscriptions to begin with.")


# Create the Application instance to be used by the bot and the processor
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

def main() -> None:
    """Start the bot."""

    # on different commands - answer in Telegram
        # Add conversation handler for subscribing
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("subscribe", start)],
        states={
            CHANNEL_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_channel_input)],
        },
        fallbacks=[CommandHandler("done", done)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("list", list_subscriptions))
    application.add_handler(CommandHandler("unsubscribe_all", unsubscribe_all))

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
