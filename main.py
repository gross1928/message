import asyncio
import multiprocessing
import os

# We need to set the working directory for the subprocesses to find the modules
project_root = os.path.dirname(os.path.abspath(__file__))

def run_bot():
    """Function to run the Telegram bot."""
    from src.bot import main
    print("Starting bot process...")
    main()

def run_client():
    """Function to run the Telethon client."""
    from src.client import main as client_main
    print("Starting client process...")
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
