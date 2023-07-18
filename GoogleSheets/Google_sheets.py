import gspread
from gspread import Cell, Client, Spreadsheet, Worksheet
from Database.DataUsers import supabase
import schedule
import threading
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/19_XAs2KCiWZXO30accQ2z0dDOW-KSVt5qDGpznXdsFw/edit#gid=0"

def rating_update():
    gc: Client = gspread.service_account("./GoogleSheets/boilerpoint-393111-68b01f6645e3.json")
    sh: Spreadsheet = gc.open_by_url(SPREADSHEET_URL)
    worksheet = sh.worksheet("📊Рейтинг")
    response = supabase.table('UsersData').select('full_name', 'balance', 'gender').execute()
    users_data = response.data
    worksheet.clear()
    worksheet.append_row(["🏆", "Аватар", "Имя", "🔘 Поинты", ])
    counter = 0
    for index, user in enumerate(users_data):
        counter+=1
        worksheet.append_row(["=СТРОКА()-1","", user['full_name'], user['balance']], value_input_option="USER_ENTERED")
        if user["gender"]:
            insert_image = '=IMAGE("https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/male.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L21hbGUucG5nIiwiaWF0IjoxNjg5NTI3MTA0LCJleHAiOjE3MjEwNjMxMDR9.Op6Tbm0ZZ_1zwCfygEAV4uOUP_bwqcXDIdGDuwViRDU&t=2023-07-16T17%3A05%3A09.763Z")'
            worksheet.update(f"B{counter+1}",[[insert_image]], value_input_option="USER_ENTERED")
        else:
            insert_image = '=IMAGE("https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/male.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L21hbGUucG5nIiwiaWF0IjoxNjg5NTI3MTA0LCJleHAiOjE3MjEwNjMxMDR9.Op6Tbm0ZZ_1zwCfygEAV4uOUP_bwqcXDIdGDuwViRDU&t=2023-07-16T17%3A05%3A09.763Z")'
            worksheet.update(f"B{counter+1}",[[insert_image]], value_input_option="USER_ENTERED")
    worksheet.sort((4, 'des'))

def rating_update_over_time():
    schedule.every(1).hour.do(rating_update)
    while True:
        schedule.run_pending()

def rating_update_start_thread():
    threading.Thread(target=rating_update_over_time).start()