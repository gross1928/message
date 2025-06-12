import asyncio
from telethon import TelegramClient
from src.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_NAME, TELEGRAM_PHONE

print("--- Telethon Session Generator ---")

# This will connect and create the .session file
client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def main():
    """Connects the client and generates the session file."""
    await client.connect()
    if not await client.is_user_authorized():
        print(f"First-time login for {TELEGRAM_PHONE}.")
        print("A code will be sent to your Telegram account.")
        await client.send_code_request(TELEGRAM_PHONE)
        try:
            await client.sign_in(TELEGRAM_PHONE, input('Please enter the code you received: '))
        except Exception as e:
            print(f"\n[ERROR] An error occurred: {e}")
            print("Please ensure your TELEGRAM_PHONE in the .env file is correct and try again.")
            return

    me = await client.get_me()
    print(f"\nSuccessfully signed in as {me.first_name} (@{me.username}).")
    print(f"Session file '{TELEGRAM_SESSION_NAME}.session' has been created successfully.")
    print("You can now stop this script (Ctrl+C).")

if __name__ == "__main__":
    print("Initializing... Make sure your .env file is populated with API_ID, API_HASH, and PHONE.")
    with client:
        client.loop.run_until_complete(main())
