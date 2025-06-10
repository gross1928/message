# Telegram Message Summarizer Bot

This bot subscribes to public Telegram channels, monitors new posts, summarizes them using OpenAI, and sends you a notification.

## Features

- Subscribe to any public Telegram channel.
- Real-time monitoring of new posts.
- AI-powered summarization with OpenAI.
- Store data in Supabase.
- Notifications with a summary and a link to the original post.

## Commands

- `/start` - Welcome message.
- `/subscribe <channel_username>` - Subscribe to a channel (e.g., `/subscribe my_channel`).
- `/list` - List all active subscriptions.
- `/unsubscribe_all` - Unsubscribe from all channels.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd message-bot
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    - Copy `.env.example` to `.env`.
    - Fill in your credentials for Telegram, Supabase, and OpenAI.

4.  **Run the bot:**
    ```bash
    python src/bot.py
    ```

## Deployment

This project is configured for deployment on Railway using a `Dockerfile`.
