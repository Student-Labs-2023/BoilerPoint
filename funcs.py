from aiogram import Bot, types
from Database.DataUsers import *
from buttons import *
from dotenv import load_dotenv
import re
from functools import lru_cache

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))

async def show_rating(chat_id: int):
    # Запрос топ 4 пользователей из БД
    top_users = supabase.table('UsersData').select('full_name', 'balance', 'tgusr').order('balance', desc = True).limit(4).execute()

    # Формируем текст рейтинга
    rating_text = "🏆 Рейтинг пользователей 🏆\n\n"
    for i, user in enumerate(top_users.data):
        position = i + 1
        full_name = user['full_name']
        balance = user['balance']
        tgusr = user['tgusr']
        rating_text += f"{position}. {full_name} ({tgusr}) - {balance} баллов\n"

    # Отправляем сообщение
    await bot.send_message(chat_id, rating_text, reply_markup=ikbmadminrating)

async def show_user_rating(chat_id: int):
    # Запрос топ 4 пользователей из БД
    top_users = supabase.table('UsersData').select('full_name', 'balance', ).order('balance', desc = True).limit(4).execute()

    # Формируем текст рейтинга
    rating_text = "🏆 Рейтинг пользователей 🏆\n\n"
    for i, user in enumerate(top_users.data):
        position = i + 1
        full_name = user['full_name']
        balance = user['balance']
        rating_text += f"{position}. {full_name}  - {balance} баллов\n"

    # Отправляем сообщение
    await bot.send_message(chat_id, rating_text, reply_markup=ikbmrating)

# Validation BAD words

standart_dirt = [1093, 1091, 1081, 124, 1073, 1083, 1103, 124, 1077, 1073, 124, 
                 1087, 1080, 1079, 1076, 124, 1105, 1073] # censored

standart_dirt = ''.join(chr(n) for n in standart_dirt)

def _get_search(pattern: str):
    @lru_cache()
    def hide_search(word: str) -> bool:
        return bool(re.search(pattern, word))

    return hide_search

def is_dirt(pattern: str=standart_dirt):

    funk = _get_search(pattern)

    def hide_search(text: str) -> bool:
        for word in re.findall(r'\w+', text):
            if funk(word.lower()):
                return True
        return False
    return hide_search



