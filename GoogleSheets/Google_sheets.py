import gspread
from gspread import Cell, Client, Spreadsheet, Worksheet
from supabase import Client, create_client
import schedule
import os
from dotenv import load_dotenv
import threading
from src.repository.usersrepository import UserRepository
from src.repository.SupabaseUserRepository import SupabaseUserRepository
from aiogram import Bot, types
from dotenv import load_dotenv
import asyncio
load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/19_XAs2KCiWZXO30accQ2z0dDOW-KSVt5qDGpznXdsFw/edit#gid=0"
ADMIN_SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1x7miGgIGGghqRQQ20Qzg37r4UGLkeHpqBUlpNRiNMmo/edit#gid=0"
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url,key)
table_name = "UsersData"
users : UserRepository = SupabaseUserRepository(supabase)

def admin_rating_udpate():
    gc: Client = gspread.service_account("./GoogleSheets/boilerpoint-393111-68b01f6645e3.json")
    sh: Spreadsheet = gc.open_by_url(ADMIN_SPREADSHEET_URL)
    worksheet = sh.worksheet("📊 Админ Рейтинг")
    response = supabase.table('UsersData').select('full_name', 'chat_id', 'tgusr', 'balance', 'gender').order('balance',desc=True).execute()
    users_data = response.data
    worksheet.clear()
    google_update_list = [["🏆", "Аватар", "Имя", "🔘 Поинты", "Чат ID", "Username"]]
    for index, user in enumerate(users_data):
        try:
            user_profile_photo = asyncio.run(bot.get_user_profile_photos(user['chat_id']))
            if len(user_profile_photo['photos'][0]) > 0:
                file = asyncio.run(bot.get_file(user_profile_photo['photos'][0][0].file_id))
                link = f'https://api.telegram.org/file/bot{os.getenv("TOKEN")}/{file.file_path}'
            else:
                if user["gender"]:
                    link = "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/male.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L21hbGUuanBnIiwiaWF0IjoxNjkxMzE5MjA5LCJleHAiOjFlKzg1fQ.YCDwpTAqL97mzSWMoPdC88KquegMuO1HPRVhUUXh3iM&t=2023-08-06T10%3A53%3A30.430Z"
                else:
                    link = "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/female.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L2ZlbWFsZS5qcGciLCJpYXQiOjE2OTEzMTkxNjMsImV4cCI6MWUrOTJ9.1LZXigPR8SlPd9Iuyy9ndoSqjbqQQmxiMES5YDu75VQ&t=2023-08-06T10%3A52%3A44.214Z"
        except:
            if user["gender"]:
                link = "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/male.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L21hbGUuanBnIiwiaWF0IjoxNjkxMzE5MjA5LCJleHAiOjFlKzg1fQ.YCDwpTAqL97mzSWMoPdC88KquegMuO1HPRVhUUXh3iM&t=2023-08-06T10%3A53%3A30.430Z"
            else:
                link = "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/female.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L2ZlbWFsZS5qcGciLCJpYXQiOjE2OTEzMTkxNjMsImV4cCI6MWUrOTJ9.1LZXigPR8SlPd9Iuyy9ndoSqjbqQQmxiMES5YDu75VQ&t=2023-08-06T10%3A52%3A44.214Z"
        if user['balance'] < 1:
            break
        if user["gender"]:
            insert_image = f'=IMAGE("{link}")'
            google_update_list.append(["=СТРОКА()-1", insert_image, user['full_name'], user['balance'],user['chat_id'],f'=ГИПЕРССЫЛКА("t.me/{user["tgusr"][1:]}";"{user["tgusr"]}")'])
        else:
            insert_image = f'=IMAGE("{link}")'
            google_update_list.append(["=СТРОКА()-1", insert_image, user['full_name'], user['balance'], user['chat_id'],f'=ГИПЕРССЫЛКА("t.me/{user["tgusr"][1:]}";"{user["tgusr"]}")'])
    worksheet.insert_rows(google_update_list, value_input_option="USER_ENTERED")
    worksheet.sort((4, 'des'))

def rating_update():
    gc: Client = gspread.service_account("./GoogleSheets/boilerpoint-393111-68b01f6645e3.json")
    sh: Spreadsheet = gc.open_by_url(SPREADSHEET_URL)
    worksheet = sh.worksheet("📊Рейтинг")
    response = supabase.table('UsersData').select('chat_id','full_name', 'balance', 'gender' ).order('balance', desc = True).execute()
    users_data = response.data
    worksheet.clear()
    google_update_list = [["🏆", "Аватар", "Имя", "🔘 Поинты"]]
    for index, user in enumerate(users_data):
        try:
            user_profile_photo = asyncio.run(bot.get_user_profile_photos(user['chat_id']))
            if len(user_profile_photo['photos'][0]) > 0:
                file = asyncio.run(bot.get_file(user_profile_photo['photos'][0][0].file_id))
                link = f'https://api.telegram.org/file/bot{os.getenv("TOKEN")}/{file.file_path}'
            else:
                if user["gender"]:
                    link = "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/male.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L21hbGUuanBnIiwiaWF0IjoxNjkxMzE5MjA5LCJleHAiOjFlKzg1fQ.YCDwpTAqL97mzSWMoPdC88KquegMuO1HPRVhUUXh3iM&t=2023-08-06T10%3A53%3A30.430Z"
                else:
                    link = "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/female.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L2ZlbWFsZS5qcGciLCJpYXQiOjE2OTEzMTkxNjMsImV4cCI6MWUrOTJ9.1LZXigPR8SlPd9Iuyy9ndoSqjbqQQmxiMES5YDu75VQ&t=2023-08-06T10%3A52%3A44.214Z"
        except:
            if user["gender"]:
                link = "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/male.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L21hbGUuanBnIiwiaWF0IjoxNjkxMzE5MjA5LCJleHAiOjFlKzg1fQ.YCDwpTAqL97mzSWMoPdC88KquegMuO1HPRVhUUXh3iM&t=2023-08-06T10%3A53%3A30.430Z"
            else:
                link = "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/female.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L2ZlbWFsZS5qcGciLCJpYXQiOjE2OTEzMTkxNjMsImV4cCI6MWUrOTJ9.1LZXigPR8SlPd9Iuyy9ndoSqjbqQQmxiMES5YDu75VQ&t=2023-08-06T10%3A52%3A44.214Z"

        if user['balance'] < 1:
            break
        if user["gender"]:
            insert_image = f'=IMAGE("{link}")'
            #insert_image = '=IMAGE("https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/male.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L21hbGUuanBnIiwiaWF0IjoxNjkxMzE5MjA5LCJleHAiOjFlKzg1fQ.YCDwpTAqL97mzSWMoPdC88KquegMuO1HPRVhUUXh3iM&t=2023-08-06T10%3A53%3A30.430Z")'
            google_update_list.append(["=СТРОКА()-1",insert_image, user['full_name'], user['balance']])
        else:
            insert_image = f'=IMAGE("{link}")'
            #insert_image = '=IMAGE("https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/female.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L2ZlbWFsZS5qcGciLCJpYXQiOjE2OTEzMTkxNjMsImV4cCI6MWUrOTJ9.1LZXigPR8SlPd9Iuyy9ndoSqjbqQQmxiMES5YDu75VQ&t=2023-08-06T10%3A52%3A44.214Z")'
            google_update_list.append(["=СТРОКА()-1", insert_image, user['full_name'], user['balance']])
    worksheet.insert_rows(google_update_list, value_input_option="USER_ENTERED")
    worksheet.sort((4, 'des'))
    admin_rating_udpate()

def rating_update_over_time():
    rating_update()
    schedule.every(10).minutes.do(rating_update)
    while True:
        schedule.run_pending()

def rating_update_start_thread():
    threading.Thread(target=rating_update_over_time).start()