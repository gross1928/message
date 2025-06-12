import asyncio
import multiprocessing
import os
import base64
import logging

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# We need to set the working directory for the subprocesses to find the modules
project_root = os.path.dirname(os.path.abspath(__file__))

# Import config after setting up the path if necessary
from src import config

def create_session_file():
    """
    Checks for a session string in env variables, decodes it,
    and writes it to a .session file.
    """
    session_string = config.TELETHON_SESSION_STRING
    if session_string:
        session_file = f"{config.TELEGRAM_SESSION_NAME}.session"
        try:
            with open(session_file, "wb") as f:
                f.write(base64.b64decode(session_string))
            logger.info(f"Successfully created session file '{session_file}' from environment variable.")
        except Exception as e:
            logger.error(f"Error decoding or writing session file: {e}")

def run_bot():
    """Function to run the Telegram bot."""
    from src.bot import main
    logger.info("Starting bot process...")
    main()

def run_client():
    """Function to run the Telethon client."""
    from src.client import main as client_main
    logger.info("Starting client process...")
    asyncio.run(client_main())

if __name__ == "__main__":
    # Create the session file from env var before starting any process
    create_session_file()

    # Create two processes
    bot_process = multiprocessing.Process(target=run_bot)
    client_process = multiprocessing.Process(target=run_client)

    # Start the processes
    bot_process.start()
    client_process.start()

    # Wait for them to complete (they won't, they run forever)
    bot_process.join()
    client_process.join()
