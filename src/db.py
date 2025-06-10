import logging
from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
logger.info("Supabase client initialized.")

def get_or_create_user(telegram_id: int, username: str = None) -> dict:
    response = supabase.table('users').upsert(
        {'telegram_id': telegram_id, 'username': username},
        on_conflict='telegram_id'
    ).execute()
    return response.data[0] if response.data else None

def get_or_create_channel(channel_username: str, channel_id: int = None) -> dict:
    """Gets a channel or creates it. Updates channel_id if provided."""
    data_to_upsert = {'channel_username': channel_username}
    if channel_id:
        data_to_upsert['channel_id'] = channel_id
    
    response = supabase.table('channels').upsert(data_to_upsert, on_conflict='channel_username').execute()
    return response.data[0] if response.data else None

def add_subscription(telegram_user_id: int, channel_username: str) -> dict:
    user = get_or_create_user(telegram_user_id)
    channel = get_or_create_channel(channel_username)

    if not user or not channel:
        return None

    response = supabase.table('subscriptions').insert({
        'user_id': user['id'],
        'channel_id': channel['id']
    }).execute()

    if '23505' in str(response.error):
        return {'error': 'already_subscribed'}
    return response.data[0] if response.data else None

def get_subscriptions(telegram_user_id: int) -> list:
    # We need a join here, which is done via RPC or careful queries.
    # For simplicity, let's get subscriptions and then channels.
    user = get_or_create_user(telegram_user_id)
    if not user:
        return []
    
    sub_response = supabase.table('subscriptions').select('channel_id').eq('user_id', user['id']).execute()
    if not sub_response.data:
        return []

    channel_ids = [sub['channel_id'] for sub in sub_response.data]
    channel_response = supabase.table('channels').select('channel_username').in_('id', channel_ids).execute()
    
    return [ch['channel_username'] for ch in channel_response.data] if channel_response.data else []

def remove_all_subscriptions(telegram_user_id: int) -> bool:
    user = get_or_create_user(telegram_user_id)
    if not user:
        return False
    
    response = supabase.table('subscriptions').delete().eq('user_id', user['id']).execute()
    return bool(response.data)

def get_all_channels() -> list:
    response = supabase.table('channels').select('channel_username').execute()
    return [ch['channel_username'] for ch in response.data] if response.data else []

def save_message(channel_id: int, message_id: int, raw_text: str, summary: str, link: str):
    response = supabase.table('messages').insert({
        'channel_id': channel_id,
        'message_id': message_id,
        'raw_text': raw_text,
        'summary': summary,
        'link': link
    }).execute()
    if '23505' in str(response.error):
        logger.warning(f"Message {message_id} from channel {channel_id} already exists.")
        return {'error': 'already_exists'}
    return response.data[0] if response.data else None

def get_subscribers_for_channel(channel_id: int) -> list:
    """Gets all telegram_ids for users subscribed to a channel."""
    sub_response = supabase.table('subscriptions').select('user_id').eq('channel_id', channel_id).execute()
    if not sub_response.data:
        return []
    
    user_ids = [sub['user_id'] for sub in sub_response.data]
    user_response = supabase.table('users').select('telegram_id').in_('id', user_ids).execute()
    
    return [user['telegram_id'] for user in user_response.data] if user_response.data else []


