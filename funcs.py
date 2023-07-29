from aiogram import Bot, types
from Database.DataUsers import *
from buttons import *
from dotenv import load_dotenv

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
    await bot.send_message(chat_id, rating_text, reply_markup=ikbmrating)

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

