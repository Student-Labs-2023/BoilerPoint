import gspread
from gspread import Cell, Client, Spreadsheet, Worksheet
from supabase import Client, create_client
import schedule
import os
from dotenv import load_dotenv
import threading
from src.repository.usersrepository import UserRepository
from src.repository.SupabaseUserRepository import SupabaseUserRepository
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/19_XAs2KCiWZXO30accQ2z0dDOW-KSVt5qDGpznXdsFw/edit#gid=0"

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url,key)
table_name = "UsersData"
users : UserRepository = SupabaseUserRepository(supabase)


def rating_update():
    gc: Client = gspread.service_account("./GoogleSheets/boilerpoint-393111-68b01f6645e3.json")
    sh: Spreadsheet = gc.open_by_url(SPREADSHEET_URL)
    worksheet = sh.worksheet("📊Рейтинг")
    response = supabase.table('UsersData').select('full_name', 'balance', 'gender' ).order('balance', desc = True).execute()
    users_data = response.data
    worksheet.clear()
    google_update_list = [["🏆", "Аватар", "Имя", "🔘 Поинты"]]
    for index, user in enumerate(users_data):
        if user['balance'] < 1:
            break
        if user["gender"]:
            insert_image = '=IMAGE("https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/male.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L21hbGUucG5nIiwiaWF0IjoxNjg5NTI3MTA0LCJleHAiOjE3MjEwNjMxMDR9.Op6Tbm0ZZ_1zwCfygEAV4uOUP_bwqcXDIdGDuwViRDU&t=2023-07-16T17%3A05%3A09.763Z")'
            google_update_list.append(["=СТРОКА()-1",insert_image, user['full_name'], user['balance']])
        else:
            insert_image = '=IMAGE("https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/female.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L2ZlbWFsZS5wbmciLCJpYXQiOjE2OTA3MDU5MjksImV4cCI6MTcyMjI0MTkyOX0.3Cu2WL8rZBXRxKU01M67DE_tmNmTlA0DvpeRnbbCyMc&t=2023-07-30T08%3A32%3A09.874Z")'
            google_update_list.append(["=СТРОКА()-1", insert_image, user['full_name'], user['balance']])
    worksheet.insert_rows(google_update_list, value_input_option="USER_ENTERED")
    worksheet.sort((4, 'des'))

def rating_update_over_time():
    rating_update()
    schedule.every(10).minutes.do(rating_update)
    while True:
        schedule.run_pending()

def rating_update_start_thread():
    threading.Thread(target=rating_update_over_time).start()