import os
import asyncio
from dotenv import load_dotenv
from supabase import Client , create_client

load_dotenv()

# Инициализация подключения к базе данных Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url,key)



def get_user_state_by_id(chat_id: int) -> str:
    try:
        response = supabase.table('UsersData').select('user_state').eq('chat_id', chat_id).limit(1).execute()
        if len(response.data) > 0:
            user_state = response.data[0].get('user_state')
            print(f"Retrieved user state for {chat_id}: {user_state}")
            return user_state
        else:
            return ""
    except Exception as e:
        print(f"Error retrieving user state for {chat_id}: {e}")
        return ""

def update_user_state(chat_id: int, state: str):
    try:
        chat_id_str = str(chat_id)  # Преобразование chat_id в строку
        response = supabase.table('UsersData').update({'user_state': state}).eq('chat_id', chat_id_str).execute()
        print(f"Updated user state for {chat_id}: {state}")
    except Exception as e:
        print(f"Error updating user state for {chat_id}: {e}")










