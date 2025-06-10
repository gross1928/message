import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_SESSION_NAME = os.getenv("TELEGRAM_SESSION_NAME", "telegram_session")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Basic validation
required_vars = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_API_ID",
    "TELEGRAM_API_HASH",
    "TELEGRAM_PHONE",
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "OPENAI_API_KEY",
]

missing_vars = [var for var in required_vars if not globals()[var]]

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
