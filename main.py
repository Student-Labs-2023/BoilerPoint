from dotenv import load_dotenv
import json
import PIL.Image
import io
import pyzbar.pyzbar as pyzbar
from aiogram import Bot, types
from io import BytesIO
import qrcode
import logging
import random
import string
import asyncio
from aiogram.utils import executor , markdown
from aiogram.utils.markdown import hlink, escape_md , code
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from typing import Optional
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import *
from pydantic import ValidationError
from src.models.users import User
from src.repository.usersrepository import UserRepository
from src.repository.SupabaseUserRepository import SupabaseUserRepository
from GoogleSheets.Google_sheets import rating_update_start_thread
from supabase import Client, create_client
#from Database.DataUsers import *
from codegen import *
from funcs import show_rating, show_user_rating

load_dotenv()
logging.basicConfig(level=logging.INFO)
# Инициализация бота, диспетчера и хранилищаа состояний
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
rating_update_start_thread()

# Инициализация подключения к базе данных Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)
table_name = "UsersData"

users: UserRepository = SupabaseUserRepository(supabase)

# Состояния регистрации
class RegistrationStates(StatesGroup):
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_name = State()
    final_reg = State()

# Состояния меню
class MenuStates(StatesGroup):
    waiting_for_profile = State()
    profile = State()
    tasks = State()
    tasks_checking = State()
    tasks_checking_question = State()
    tasks_solving = State()
    calendar = State()
    help = State()
    help_start = State()
    help_end = State()
    help_cancel = State()
    help_ender = State()
    rating = State()
    promocode = State()
    promocodestart = State()

# Состояние удаления профиля
class ProlfileStates(StatesGroup):
    profile_menu_main_state = State()
    delete_profile = State()
    edit_profile = State()
    edit_profile_name = State()
    edit_profile_age = State()

# Состояния админ-панели
class AdminPanel(StatesGroup):
    admin_menu = State()
    change_user = State()
    change_user_end = State()
    get_info_about_user_start = State()
    get_info_about_user = State()
    get_info_about_user_end = State()
    change_user_start = State()
    change_user_fullname = State()
    change_user_fullnamestart = State()
    change_user_age = State()
    change_user_agestart = State()
    change_user_balance = State()
    change_user_balancestart = State()
    update_users_balance_confirm = State()
    update_users_balance = State()
    promo_menu = State()
    promo_check_promocode = State()
    promo_addpromostart = State()
    promo_addpromo_naming = State()
    promo_addpromo_naming_usages = State()
    promo_addpromo_naming_cost = State()
    promo_addpromo_naming_end = State()
    promo_addpromousages = State()
    promo_addpromocost = State()
    promo_addpromoend = State()
    promo_delpromo = State()
    promo_qr = State()
    promo_qrstart = State()
    promo_qrend = State()
    add_event = State()
    add_task = State()
    backward = State()
    rating_board = State()
    ticket = State()
    ticket_check = State()
    ticket_delete = State()
    ticket_start = State()
    ticket_middle = State()
    ticket_end = State()
    rules = State()
    rules_addmaker = State()
    rules_addmaker_start = State()
    rules_delmaker = State()
    rules_delmaker_start = State()

class EventMakerPanel(StatesGroup):
    menu = State()
    add = State()
    delete = State()

@dp.message_handler(commands=['event'], state='*')
async def event_command(message: types.Message, state: FSMContext):
    with open('roles.json') as f:
        event_roles = json.load(f)['event_makers']

    if str(message.from_user.id) not in event_roles:
        await message.reply("У вас нет прав event maker'а!", reply_markup=rkbm)
        return

    await EventMakerPanel.menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(EventMakerPanel.menu)
    users.set(user)
    await message.reply("Вы вошли в панель event maker`a!", reply_markup=usermakerkbm)

@dp.message_handler(text = "⬅️Меню", state=EventMakerPanel.menu)
async def back_from_event(message: types.Message, state:FSMContext):
    await MenuStates.waiting_for_profile.set()
    user = users.get(message.chat.id)
    user.user_state = str(MenuStates.waiting_for_profile)
    users.set(user)
    await message.reply("Вы вышли из панели event maker`a", reply_markup=rkbm)

# Хендлер отмены действия через кнопку
@dp.callback_query_handler(text="cancel", state=[AdminPanel.change_user_balance,AdminPanel.change_user_fullname,AdminPanel.change_user_agestart,AdminPanel.get_info_about_user])
async def cancel_action(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено, вы вернулись в меню админ-панели.", reply_markup=admrkbm)
    await AdminPanel.admin_menu.set()

@dp.message_handler(commands=['admin'], state='*')
async def admin_command(message: types.Message, state: FSMContext):
    # Проверка, что пользователь в списке админов
    with open('roles.json') as f:
        admin_roles = json.load(f)['admins']

    if str(message.from_user.id) not in admin_roles:
        await message.reply("У вас нет прав администратора!", reply_markup=rkbm)
        return

    # Установка состояния и вывод кнопок админки
    await AdminPanel.admin_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.admin_menu)
    users.set(user)
    await message.reply("Вы вошли в панель администратора", reply_markup=admrkbm)

@dp.message_handler(text="❗Обнулить баланс всех пользователей❗", state=[AdminPanel.change_user_start, AdminPanel.change_user_end])
async def update_users_balance_confirm(message: types.Message,state:FSMContext):
    await AdminPanel.update_users_balance_confirm.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.update_users_balance)
    users.set(user)
    await bot.send_message(message.chat.id, '❗Внимание❗ Вы действительно хотите обнулить баланс ВСЕХ пользователей? Данное действие ОТМЕНИТЬ будет НЕВОЗМОЖНО', reply_markup=updatebalanceusers)
    await AdminPanel.update_users_balance.set()

@dp.message_handler(state=AdminPanel.update_users_balance)
async def update_users_balance(message: types.Message,state:FSMContext):
    await AdminPanel.update_users_balance.set()
    select = message.text
    if select == '❗Я действительно хочу обнулить баланс всех пользователей!❗ ВНИМАНИЕ❗Отменить данное действие будет НЕВОЗМОЖНО.❗':
        supabase.table('UsersData_duplicate').update({'balance': 0}).neq('balance',0).execute()
        await AdminPanel.admin_menu.set()
        user = users.get(message.chat.id)
        user.user_state = str(AdminPanel.admin_menu)
        users.set(user)
        await message.reply("Баланс всех пользователей равен 0!", reply_markup=admrkbm)
    elif select == '⬅️Назад в меню':
        await AdminPanel.admin_menu.set()
        user = users.get(message.chat.id)
        user.user_state = str(AdminPanel.admin_menu)
        users.set(user)
        await message.reply("Вы вернулись в панель администратора", reply_markup=admrkbm)
    else:
        await message.reply("Нет такого варианта, ошибка!")
       


# Хендлер для кнопки  ️Изменить пользователя
@dp.message_handler(text="⚙️Изменить пользователя", state=AdminPanel.admin_menu)
async def admin_change_user(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_start.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.change_user_start)
    users.set(user)
    await message.reply(
        "Вы попали в меню редактирования пользователя, нажмите нужную вам кнопку чтобы изменить параметры пользователя. После нажатия на кнопку введите @username человека в телеграм чтобы поменять его параметры.",
        reply_markup=admue)

@dp.message_handler(text="Получить информацию о пользователе", state=[AdminPanel.change_user_start, AdminPanel.change_user_end])
async def admin_get_user_info(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = users.get(chat_id) 
    user.user_state = str(AdminPanel.get_info_about_user)
    await message.reply("Введите @username пользователя о котором хотите получить информацию", reply_markup=types.ReplyKeyboardRemove())
    await message.reply("Для отмены действия, нажмите кнопку отмена", reply_markup=InlineKeyboardMarkup().add(cancel_button))
    await AdminPanel.get_info_about_user.set()
    users.set(user)

@dp.message_handler(state=AdminPanel.get_info_about_user)
async def admin_get_user_info_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    username = message.text
    user = users.get(chat_id)
    user.user_state = str(AdminPanel.get_info_about_user_start)
    try:
        userinfo = users.get(username)
        userlist = supabase.table('UsersData').select('chat_id').order('balance', desc=True).execute().data
        counter = 0
        while userlist[counter]['chat_id'] != userinfo.chat_id:
            counter += 1
        pseudo = userinfo.full_name
        gender = userinfo.gender
        age = userinfo.age
        balance = userinfo.balance
        if gender:
            gender = "🙋‍♂️"
            image = os.environ.get("MALE")
        else:
            gender = "🙋‍♀️"
            image = os.environ.get("FEMALE")
            # Формирование сообщения профиля пользователя
        profile_message = f"Профиль пользователя {username}:\n\n" \
        f"{gender}{pseudo}, {age} лет\n└Место в топе: {counter+1}\n\n" \
        f"💰Баланс: {balance}🔘 поинтов\n└Мероприятий посещено: ?"
        await bot.send_photo(chat_id=chat_id, photo=image, caption=profile_message, reply_markup=admue)
        await AdminPanel.get_info_about_user_end.set()
        user.user_state = str(AdminPanel.get_info_about_user_end)
        users.set(user)
        await state.finish()
        await AdminPanel.change_user_start.set()
    except IndexError:
        await message.reply("Такого пользователя не существует. ", reply_markup=admue)
        await AdminPanel.change_user_start.set()
        user.user_state = str(AdminPanel.change_user_start)
        users.set(user)
    
@dp.message_handler(text="Изменить баланс", state=[AdminPanel.change_user_start, AdminPanel.change_user_end])
async def admin_change_user_balance(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_balancestart.set()
    await message.reply("Введите @username пользователя, которого необходимо отредактировать", reply_markup=types.ReplyKeyboardRemove())
    admin = users.get(message.chat.id)
    admin.user_state = str(AdminPanel.change_user_balancestart)
    users.set(admin)

@dp.message_handler(state=AdminPanel.change_user_balancestart)
async def admin_change_user_balance_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    try:
        userinfo = users.get(username)
        await state.update_data(username=username)
        await AdminPanel.change_user_balance.set()
        await message.reply("Введите новый баланс пользователя", reply_markup=InlineKeyboardMarkup().add(cancel_button))
        admin = users.get(message.chat.id)
        admin.user_state = str(AdminPanel.change_user_balance)
        users.set(admin)
    except IndexError:
        await message.reply("Такого пользователя нет в базе данных", reply_markup=admue)
        await state.finish()
        await AdminPanel.change_user_start.set()
        return

@dp.message_handler(state=AdminPanel.change_user_balance)
async def admin_change_user_balance_handler(message: types.Message, state: FSMContext):
    new_balance = message.text
    data = await state.get_data()
    username = data.get("username")
    userinfo = users.get(username)
    userinfo.balance = new_balance
    users.set(userinfo)
    #   Отправляем сообщение об успешном обновлении
    await state.finish()
    await AdminPanel.change_user_end.set()
    admin = users.get(message.chat.id)
    admin.user_state = str(AdminPanel.change_user_end)
    users.set(admin)
    await message.reply(f"Баланс пользователя {username} успешно обновлен на {new_balance}", reply_markup=admue)

# Хендлер для смены фио через админа

@dp.message_handler(text="Изменить ФИО", state=[AdminPanel.change_user_start, AdminPanel.change_user_end])
async def admin_change_user_fullname(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_fullnamestart.set()
    await message.reply("Введите @username пользователя, которого необходимо отредактировать", reply_markup=types.ReplyKeyboardRemove())
    admin = users.get(message.chat.id)
    admin.user_state = str(AdminPanel.change_user_fullnamestart)
    users.set(admin)

@dp.message_handler(state=AdminPanel.change_user_fullnamestart)
async def admin_change_user_fullname_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    try:
        userinfo = users.get(username)
        await state.update_data(username=username)  # сохраняем username в данных состояния
        await AdminPanel.change_user_fullname.set()  # переходим к следующему состоянию
        await message.reply("Введите новое ФИО пользователя", reply_markup=InlineKeyboardMarkup().add(cancel_button))
        user = users.get(message.chat.id)
        user.user_state = str(AdminPanel.change_user_fullname)
        users.set(user)
    except IndexError:
        await message.reply("Такого пользователя нет в базе данных", reply_markup=admue)
        await state.finish()
        await AdminPanel.change_user_start.set()
        return
    # Проверяем, есть ли такой пользователь

@dp.message_handler(state=AdminPanel.change_user_fullname)
async def admin_change_user_fullname_handler(message: types.Message, state: FSMContext):
    new_fullname = message.text  # получаем новое ФИО
    chat_id = message.chat.id
    admin = users.get(chat_id)
    if new_fullname.replace(" ", "").isalpha() and len(new_fullname) < 40:
        data = await state.get_data()
        username = data.get("username")  # получаем сохраненный username из данных состояния
        userinfo = users.get(username)
        userinfo.full_name = new_fullname
        admin.user_state = str(AdminPanel.change_user_end)
        users.set(admin)
        users.set(userinfo)
        # Отправляем сообщение об успешном обновлении
        await message.reply(f"ФИО пользователя {username} успешно обновлено на {new_fullname}", reply_markup=admue)
        await state.finish()
        await AdminPanel.change_user_end.set()
    else:
        await message.reply("Неккоректное ФИО")
        await AdminPanel.change_user_fullname.set()
        user = users.get(message.chat.id)
        user.user_state = str(AdminPanel.change_user_fullname)
        users.set(user)

# Хендлер для смены возраста через админ меню
@dp.message_handler(text="Изменить возраст", state=[AdminPanel.change_user_start, AdminPanel.change_user_end])
async def admin_change_user_age(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_age.set()
    admin = users.get(message.chat.id)
    admin.user_state = str(AdminPanel.change_user_age)
    users.set(admin)
    await message.reply("Введите @username пользователя, которого необходимо отредактировать", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=AdminPanel.change_user_age)
async def admin_change_user_age_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    try:
        userinfo = users.get(username)
        await state.update_data(username=username)  # сохраняем username в данных состояния
        await AdminPanel.change_user_agestart.set()  # переходим к следующему состоянию
        admin = users.get(message.chat.id)
        admin.user_state = str(AdminPanel.change_user_agestart)
        users.set(admin)
        await message.reply("Введите новый возраст пользователя", reply_markup=InlineKeyboardMarkup().add(cancel_button))
        
    # Проверяем, есть ли такой пользователь
    except IndexError:
        await message.reply("Такого пользователя нет в базе данных", reply_markup=admue)
        await state.finish()
        await AdminPanel.change_user_start.set()
        return

@dp.message_handler(state=AdminPanel.change_user_agestart)
async def admin_change_user_age_handler(message: types.Message, state: FSMContext):
    new_age = message.text  # получаем новый возраст
    try:
        new_age = int(new_age)
    except ValueError as e:
        await message.reply("Ваш возраст неккоректен. Возраст не должен содержать буквы!")
        print(f"Error validation age{e}")
    if new_age < 12 or new_age > 122:
        await message.reply("Ваш возраст неккоректен. Возраст должен лежать в диапазоне от 12 - 122")
        await AdminPanel.change_user_agestart.set()
    else:
        data = await state.get_data()
        username = data.get("username")  # получаем сохраненный username из данных состояния
        user = users.get(username)
        user.age = new_age
        user.user_state = str(AdminPanel.change_user_end)
        users.set(user)
        # Отправляем сообщение об успешном обновлении
        await message.reply(f"Возраст пользователя {username} успешно обновлен на {new_age}", reply_markup=admue)
        await state.finish()
        await AdminPanel.change_user_end.set()

# Хендлер для входа в меню промокодов
@dp.message_handler(text="🗝️Промокоды", state=AdminPanel.admin_menu)
async def admin_promocodes(message: types.Message, state: FSMContext):
    await AdminPanel.promo_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.promo_menu)
    users.set(user)
    await message.reply("Вы вошли в меню промокодов", reply_markup=admpromo)

@dp.message_handler(text="Добавить QR", state=AdminPanel.promo_menu)
async def admin_promocodes_addqr(message: types.Message, state: FSMContext):
    await AdminPanel.promo_qrstart.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.promo_qrstart)
    users.set(user)
    await message.reply("Введите промокод, который хотите помстить в QR-код", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=AdminPanel.promo_qrstart)
async def admin_promocodes_add_qr_set(message: types.Message, state: FSMContext):
    promo_code = message.text
    promocode_data = supabase.table('Promocode').select('cost').eq('promo', promo_code).execute()

    if not promocode_data.data or promocode_data.data[0]['cost'] == 0:
        await message.reply("Такого промокода не существует или лимит его использования исчерпан", reply_markup=admpromo)
        await state.finish()
        await AdminPanel.promo_menu.set()
        return

    qr = qrcode.make(promo_code)

    byte_io = BytesIO()
    qr.save(byte_io, 'PNG')
    byte_io.seek(0)

    await message.reply_photo(byte_io, caption="Вот QR\\-код для промокода " + code(promo_code) , reply_markup=admpromo, parse_mode="MarkdownV2")

    byte_io.close()

    await state.finish()
    await AdminPanel.promo_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.promo_menu)

@dp.message_handler(text="Действующие промокоды", state=AdminPanel.promo_menu)
async def admin_promocodes_check(message: types.Message, state: FSMContext):
    await AdminPanel.promo_check_promocode.set()
    chat_id = message.chat.id
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.promo_check_promocode)

    promos = supabase.table('Promocode').select('promo', 'last', 'cost').filter('last', 'gt', 0).order('cost', desc=True).execute()

    promo_text = "📝 Действующие промокоды:\n\n"

    for promo in promos.data:
        codee = promo['promo']
        uses_left = promo['last']
        cost = promo['cost']

        promo_text += (code(f"{codee}") + f" \\- {uses_left} исп\\.\\, {cost} поинтов\n")

    await bot.send_message(chat_id, promo_text, parse_mode="MarkdownV2", reply_markup=admpromo)
    supabase.table('Promocode').delete().eq('last', 0).execute()
    await state.finish()
    await AdminPanel.promo_menu.set()
    user.user_state = str(AdminPanel.promo_menu)

@dp.message_handler(text='Нэйминг-промо', state=AdminPanel.promo_menu)
async def get_naming_promo(message: types.Message, state: FSMContext):
    await message.reply("Введите имя промокода", reply_markup=types.ReplyKeyboardRemove())
    user = users.get(message.chat.id)
    await AdminPanel.promo_addpromo_naming.set()

@dp.message_handler(state=AdminPanel.promo_addpromo_naming)
async def get_naming_promo_usages(message: types.Message, state:FSMContext):
    name = str(message.text)
    await message.reply("Введите количество использований:")
    await state.update_data(name=name)
    await AdminPanel.promo_addpromo_naming_cost.set()

@dp.message_handler(state=AdminPanel.promo_addpromo_naming_cost)
async def get_naming_promo_cost(message: types.Message, state:FSMContext):
    usages = int(message.text)
    await message.reply("Введите цену промокода:")
    await state.update_data(usages=usages)
    await AdminPanel.promo_addpromo_naming_end.set()

@dp.message_handler(state=AdminPanel.promo_addpromo_naming_end)
async def create_naming_promo(message: types.Message, state:FSMContext):
    cost = int(message.text)
    data = await state.get_data()
    name = data.get("name")
    usages = data.get("usages")
    codee = generate_naming_promo(name, usages, cost)

    texting = (f'Промокод '+ code(f"{codee}") + f' с {usages} использованиями и ценой {cost} создан')
    await message.reply(texting, reply_markup=admpromo, parse_mode= "MarkdownV2")
    await state.finish()
    await AdminPanel.promo_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.promo_menu)

@dp.message_handler(text ='Добавить промокод',state=AdminPanel.promo_menu)
async def get_usages(message: types.Message, state: FSMContext):
    await message.reply("Введите количество использований:", reply_markup=types.ReplyKeyboardRemove())
    await AdminPanel.promo_addpromousages.set()

@dp.message_handler(state=AdminPanel.promo_addpromousages)
async def get_cost(message: types.Message, state: FSMContext):
    usages = int(message.text)
    await message.reply("Введите цену промокода:")
    await state.update_data(usages=usages)
    await AdminPanel.promo_addpromocost.set()

@dp.message_handler(state=AdminPanel.promo_addpromocost)
async def create_promo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    usages = data.get("usages")
    cost = int(message.text)

    codee = generate_promo(usages, cost)

    texting = (f'Промокод ' + code(f"{codee}") + f' с {usages} использованиями и ценой {cost} создан')
    await message.reply(texting, reply_markup=admpromo, parse_mode="MarkdownV2")
    await state.finish()
    await AdminPanel.promo_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.promo_menu)

@dp.message_handler(text="Удалить промокод", state=AdminPanel.promo_menu)
async def delete_promo(message: types.Message, state: FSMContext):
    await AdminPanel.promo_delpromo.set()
    await message.reply("Введите промокод для удаления", reply_markup=types.ReplyKeyboardRemove())
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.promo_delpromo)
    users.set(user)


@dp.message_handler(state=AdminPanel.promo_delpromo)
async def delete_promo_handler(message: types.Message, state: FSMContext):
    code = message.text
    deleted = supabase.table('Promocode').delete().match({'promo': code}).execute()

    if not deleted.data:
        # ничего не удалено
        await message.reply("Промокод не найден", reply_markup=admpromo)
        await state.finish()
        await AdminPanel.promo_menu.set()
        return

    # удаление прошло успешно
    await message.reply(f"Промокод {code} удален", reply_markup=admpromo)
    await AdminPanel.promo_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.promo_menu)

# Хедлер для бека в меню админа
@dp.message_handler(text="⬅️Админ меню", state=[AdminPanel.change_user_start, AdminPanel.change_user_end, AdminPanel.promo_menu])
async def admin_backtomenu(message: types.Message, state: FSMContext):
    await message.reply("Вы вернулись в админ меню", reply_markup=admrkbm)
    await AdminPanel.admin_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.admin_menu)
    users.set(user)

@dp.message_handler(text="👨‍🚀Организаторы", state=AdminPanel.admin_menu)
async def give_ruleskbm(message: types.Message, state:FSMContext):
    await AdminPanel.rules.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.rules)
    users.set(user)
    await message.reply("Вы попали в раздел для выдачи права создания заданий пользователям. Нажмите на кнопку и следуйте указаниям.", reply_markup=ruleskbm)

@dp.message_handler(text="Выдать права",state = AdminPanel.rules)
async def give_rules(message: types.Message, state: FSMContext):
    await AdminPanel.rules_addmaker.set()
    await message.reply("Введите @username пользователя которому хотите выдать права ивент мейкера", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AdminPanel.rules_addmaker)
async def give_rules_start(message: types.Message, state: FSMContext):
    tgusr = message.text

    user_data = supabase.table('UsersData').select('chat_id').eq('tgusr', tgusr).execute()

    if not user_data.data:
        await message.reply("Пользователя с таким @username не существует", reply_markup=ruleskbm)
        await state.finish()
        await AdminPanel.rules.set()
        return

    chat_id = user_data.data[0]['chat_id']

    with open('roles.json', 'r') as f:
        roles = json.load(f)

    roles['event_makers'].append(str(chat_id))

    with open('roles.json', 'w') as f:
        json.dump(roles, f)

    await message.reply("Права выданы успешно", reply_markup=ruleskbm)

    await state.finish()
    await AdminPanel.rules.set()

@dp.message_handler(text="Забрать права", state=AdminPanel.rules)
async def del_from_eventers(message: types.Message, state:FSMContext):
    await AdminPanel.rules_delmaker.set()
    await message.reply("Введите @username пользователя у котрого хотите забрать права",reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=AdminPanel.rules_delmaker)
async def del_from_eventers_start(message: types.Message, state: FSMContext):
  tgusr = message.text

  user_data = supabase.table('UsersData').select('chat_id').eq('tgusr', tgusr).execute()

  if not user_data.data:
    await message.reply("Пользователя с таким username не существует", reply_markup=ruleskbm)
    await state.finish()
    await AdminPanel.rules.set()
    return

  chat_id = user_data.data[0]['chat_id']

  with open('roles.json', 'r') as f:
    roles = json.load(f)

  if str(chat_id) in roles['event_makers']:
    roles['event_makers'].remove(str(chat_id))

  with open('roles.json', 'w') as f:
    json.dump(roles, f)

  await message.reply("Права успешно удалены", reply_markup=ruleskbm)

  await state.finish()
  await AdminPanel.rules.set()

@dp.message_handler(text='Действующие права', state=AdminPanel.rules)
async def show_rules(message: types.Message, state: FSMContext):

  with open('roles.json', 'r') as f:
    roles = json.load(f)

  event_makers = roles['event_makers']

  rules_text = "📝 Пользователи с правами ивент-мейкера:\n\n"

  for chat_id in event_makers:
    user_data = supabase.table('UsersData').select('tgusr').eq('chat_id', int(chat_id)).execute()
    if user_data.data:
      username = user_data.data[0]['tgusr']
      rules_text += f"{username} - {chat_id}\n"

  await message.reply(rules_text)
  await state.finish()
  await AdminPanel.rules.set()

@dp.message_handler(text="⬅️Админ меню", state=AdminPanel.rules)
async def back_from_rules(message: types.Message, state: FSMContext):
    await message.reply("Вы вернулись в админ меню", reply_markup=admrkbm)
    await AdminPanel.admin_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.admin_menu)
    users.set(user)

@dp.message_handler(text="⬅️Меню", state=AdminPanel.admin_menu)
async def admin_menu_back(message: types.Message, state: FSMContext):
    await MenuStates.waiting_for_profile.set()
    user = users.get(message.chat.id)
    user.user_state = str(MenuStates.waiting_for_profile)
    users.set(user)
    await message.reply("Вы вышли из панели администратора", reply_markup=rkbm)

@dp.message_handler(text="📊Рейтинг", state=AdminPanel.admin_menu)
async def admin_rating_board(message: types.Message, state: FSMContext):
    await AdminPanel.rating_board.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.rating_board)
    users.set(user)
    await show_rating(message.chat.id)
    await AdminPanel.admin_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.admin_menu)
    users.set(user)

@dp.message_handler(Command('start'), state=None)
async def start_command(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = users.get(id=chat_id)  # Получение состояния пользователя из Supabase

    if user and not (user.full_name == ""):
        # Пользователь уже зарегистрирован
        await MenuStates.waiting_for_profile.set()
        await message.reply("Чтобы просмотреть свой профиль, нажмите кнопку 'Профиль'.", reply_markup=rkbm)
    else:
        user = user if user else User(chat_id=chat_id)

        # Сохранение состояния пользователя
        telegram_name = message.from_user.username

        user.user_state = str(RegistrationStates.waiting_for_age)
        if telegram_name == None:
            user.tgusr = "У пользователя нет имени"
        else:
            user.tgusr = "@" + telegram_name
        users.set(user)

        # Регистрация нового пользователя
        await message.reply("Привет! Давай зарегистрируемся! Введите ваш возраст:")
        # Установка состояния "waiting_for_age" для пользователя
        await RegistrationStates.waiting_for_age.set()

@dp.message_handler(state=RegistrationStates.waiting_for_age)
async def handle_age(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    age = message.text
    try:
        age = int(age)
    except ValueError as e:
        await bot.send_message(chat_id, "Ваш возраст неккоректен. Возраст не должен содержать буквы!")
        print(f"Error validation age{e}")
    if age < 12 or age > 122:
        await bot.send_message(chat_id, "Ваш возраст неккоректен. Возраст должен лежать в диапазоне от 12 - 122")
        await RegistrationStates.waiting_for_age.set()
    else:
        user = users.get(chat_id)
        user.age = age
        # Сохранение возраста пользователя в DTO
        print(f"Возраст пользователя {chat_id}: {age}")

        # Переход к следующему состоянию "waiting_for_gender"
        await RegistrationStates.waiting_for_gender.set()
        # Сохранение состояния пользователя
        user.user_state = str(RegistrationStates.waiting_for_gender)
        users.set(user)

        # Запрашиваем пол пользователя
        await message.reply("Введите ваш пол (Male/Female):", reply_markup=ikbg)

@dp.message_handler(state=RegistrationStates.waiting_for_gender)
async def handle_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender not in ["мужской", "женский"]:
        await message.reply("Пол указан некорректно. Выберите пол кнопками ниже:", reply_markup=ikbg)
        return

@dp.callback_query_handler(state=RegistrationStates.waiting_for_gender)
async def handle_gender_callback(query: types.CallbackQuery, state: FSMContext):
    chat_id = query.message.chat.id
    gender = query.data.lower()
    user = users.get(chat_id)
    user.gender = bool(int(gender))
    print(f"Пол пользователя {chat_id}: {gender}")

    # Запрашиваем имя пользователя
    await query.message.reply("Введите ваше ФИО:")

    # Переход к следующему состоянию "waiting_for_name"
    await RegistrationStates.waiting_for_name.set()
    user.user_state = str(RegistrationStates.waiting_for_name)
    users.set(user)

@dp.message_handler(state=RegistrationStates.waiting_for_name)
async def handle_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    name = message.text
    if name.replace(" ", "").isalpha() and len(name) < 40:
        user = users.get(chat_id)
        user.full_name = name
        user.user_state = str(RegistrationStates.final_reg)  # по сути финал рег нафиг не нужен
        users.set(user)

        print(f"Имя пользователя {chat_id}: {name}")
        # Отправка сообщения о успешной регистрации
        if str(message.from_user.username) == 'None':
            await bot.send_message(chat_id,
                                   f"Регистрация успешно завершена с неточностями, {user.full_name}!У вас нет имени пользователя Телеграм, связь администрации с вами может быть усложнена, вам необходимо указать в вашем профиле телеграма ваше имя пользователя и перерегистрироваться в боте.",
                                   reply_markup=rkbm)
        else:
            await bot.send_message(chat_id, f"Регистрация успешно завершена, {user.full_name}!", reply_markup=rkbm)
        await state.finish()
        await MenuStates.waiting_for_profile.set()
    else:
        await bot.send_message(chat_id, f"Пожалуйста, введите корректно свое ФИО")
        await RegistrationStates.waiting_for_name.set()

@dp.message_handler(state=MenuStates.waiting_for_profile)
async def handle_waiting_for_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    if select == "👤Профиль":
        await MenuStates.profile.set()
        await handle_profile(message, state)
    elif select == "📊Рейтинг":
        await MenuStates.rating.set()
        await user_rating_board(message, state)
    elif select =="❓Помощь":
        await MenuStates.help.set()
        await handle_help(message,state)
    elif select == "📆Календарь событий":
        await MenuStates.calendar.set()
        await handle_calendar(message, state)
    elif select == "📝Задания":
        counter_data = supabase.table('Pointer').select('chat_id').eq('chat_id', chat_id).execute()
        if not counter_data.data:
            supabase.table('Pointer').insert({'chat_id': chat_id, 'counter': 0}).execute()
        else:
            supabase.table('Pointer').update({'counter': 0}).eq('chat_id', chat_id).execute()
        await MenuStates.tasks.set()
        await handle_tasks(message, state)
    elif select == "🗝️Промокоды":
        await MenuStates.promocode.set()
        await bot.send_message(chat_id, "Вы попали в меню работы с промокодами", reply_markup=promo_kb)
    else:
        await message.reply("Нет такого варианта выбора!", reply_markup=rkbm)

@dp.callback_query_handler(text="cancel_user", state=[ProlfileStates.edit_profile_name, ProlfileStates.edit_profile_age])
async def cancel_action(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено, вы вернулись в меню редактирования профиля.", reply_markup=menuedit)
    await ProlfileStates.edit_profile.set()

@dp.callback_query_handler(text='back_to_menu', state = MenuStates.promocodestart)
async def cancel_action(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено, вы вернулись в меню промокодов.", reply_markup=promo_kb)
    await MenuStates.promocode.set()

@dp.callback_query_handler(text="cancel_user_help", state=MenuStates.help_end)
async def cancel_action(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено, вы вернулись в меню помощи.", reply_markup=userhelp)
    await MenuStates.help_cancel.set()

@dp.message_handler(state=ProlfileStates.edit_profile)
async def handle_waiting_for_edit_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    if select == "Изменить ФИО":
        await ProlfileStates.edit_profile_name.set()
        await bot.send_message(chat_id, "Вы выбрали редактирование ФИО", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id, "Введите новое ФИО ", reply_markup=cancel_button_for_user)
    elif select == "Изменить возраст":    
        await ProlfileStates.edit_profile_age.set()
        await bot.send_message(chat_id, "Вы выбрали редактирование возраста", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id, "Введите новый возраст ", reply_markup=cancel_button_for_user)
    elif select == "⬅️Назад в меню":
        await MenuStates.waiting_for_profile.set()
        await bot.send_message(chat_id, "Вы вышли в меню! ", reply_markup=rkbm)
    else:
        await message.reply("Нет такого варианта выбора!")

@dp.message_handler(state=ProlfileStates.edit_profile_name)
async def edit_name_profile(message: types.Message, state:FSMContext):
    new_fullname = message.text  
    chat_id = message.chat.id
    if new_fullname.replace(" ", "").isalpha() and len(new_fullname) < 40:
        user = users.get(chat_id)
        user.full_name = new_fullname
        user.user_state = str(ProlfileStates.edit_profile_name)
        users.set(user)
        await message.reply(f"Имя успешно обновлено на : {new_fullname}", reply_markup=rkbm)
        await state.finish()
        await MenuStates.waiting_for_profile.set()

@dp.message_handler(state=ProlfileStates.edit_profile_age)
async def edit_age_profile(message: types.Message, state: FSMContext):
    new_age = message.text  # получаем новый возраст
    try:
        new_age = int(new_age)
    except ValueError as e:
        await message.reply("Ваш возраст неккоректен. Возраст не должен содержать буквы!")
        print(f"Error validation age{e}")
    if new_age < 12 or new_age > 122:
        await message.reply("Ваш возраст неккоректен. Возраст должен лежать в диапазоне от 12 - 122")
        await ProlfileStates.edit_profile_age.set()
    else:
        chat_id = message.chat.id
        user = users.get(chat_id)
        user.age = new_age
        user.user_state = str(ProlfileStates.edit_profile_age)
        users.set(user)
        # Отправляем сообщение об успешном обновлении
        await message.reply(f"Возраст успешно обновлен на {new_age}", reply_markup=rkbm)
        await state.finish()
        await MenuStates.waiting_for_profile.set()

@dp.message_handler(text="🗝️Ввести промокод", state=MenuStates.promocode)
async def enter_promocode(message: types.Message):
    await bot.send_message(message.chat.id, "Введите , пожалуйста , ваш промокод сообщением или отправьте боту изображение QR-кода", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, "Если хотите вернуться , то нажмите сюда", reply_markup=cancel_button_to_main)
    await MenuStates.promocodestart.set()

@dp.message_handler(content_types=['photo'], state=MenuStates.promocodestart)
async def check_qr_code(message: types.Message, state: FSMContext):

  photo_bytes = await message.photo[-1].download(destination=io.BytesIO())
  photo_bytes = photo_bytes.getvalue()

  photo_image = PIL.Image.open(io.BytesIO(photo_bytes))

  qr_code = pyzbar.decode(photo_image)

  if qr_code:
    qr_code = qr_code[0].data.decode()

  message.text = qr_code
  await check_promocode(message, state)

@dp.message_handler(state=MenuStates.promocodestart)
async def check_promocode(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    promocode = message.text
    poro = promocode

    user = users.get(chat_id)
    balance_result = supabase.table('UsersData').select('balance').eq('chat_id', chat_id).execute()
    bal = balance_result.data[0]['balance']
    balance = int(bal)

    promocode_data = supabase.table('Promocode').select('last', 'cost').eq('promo', promocode).execute()

    if not promocode_data.data:
        await message.reply("Промокод не найден!", reply_markup=promo_kb)
        await state.finish()
        await MenuStates.promocode.set()
        user.user_state = str(MenuStates.promocode)  # Меню стейт
        users.set(user)
        return

    promocode = promocode_data.data[0]

    used_promocode_data = supabase.table('UsedPromocode').select('chat_id').eq('promo', poro).eq('chat_id', chat_id).execute()

    if used_promocode_data.data:
        # уже использовал
        await message.reply("Вы уже использовали этот промокод!", reply_markup=promo_kb)
        await state.finish()
        await MenuStates.promocode.set()
        user.user_state = str(MenuStates.promocode)  # Меню стейт
        users.set(user)
        return

    if promocode['last'] <= 0:
        await message.reply("Срок действия промокода истек!", reply_markup=promo_kb)
        await state.finish()
        await MenuStates.promocode.set()
        user.user_state = str(MenuStates.promocode)  # Меню стейт
        users.set(user)
        return

    new_balance = balance + promocode['cost']
    print(new_balance)

    new_last = promocode['last'] - 1
    
    user.balance = new_balance
    # Добавим запись о том, что промокод был использован данным пользователем
    supabase.table('Promocode').update({'last': new_last}).eq('promo', poro).execute()
    expression = ''.join(random.choices(string.ascii_letters, k=8))
    supabase.table('UsedPromocode').insert({'id' : expression,'promo': poro, 'chat_id': str(chat_id)}).execute()

    await message.reply(f"Ваш баланс пополнен на {promocode['cost']}!", reply_markup=promo_kb)

    await state.finish()
    await MenuStates.promocode.set()
    user.user_state = str(MenuStates.promocode)  # Меню стейт
    users.set(user)

@dp.message_handler(text="⬅️Назад в меню", state=MenuStates.promocode)
async def back_from_promo_menu(message: types.Message, state: FSMContext):
    await MenuStates.waiting_for_profile.set()
    await bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=rkbm)


@dp.message_handler(text ="📊Рейтинг", state=MenuStates.waiting_for_profile)
async def user_rating_board(message: types.Message, state: FSMContext):
    await MenuStates.rating.set()
    user = users.get(message.chat.id)
    user.user_state = str(MenuStates.rating)
    users.set(user)
    await show_user_rating(message.chat.id)
    await MenuStates.waiting_for_profile.set()
    user = users.get(message.chat.id)
    user.user_state = str(MenuStates.waiting_for_profile)
    users.set(user)

#-----------------------------------------------------------------------------------------------------------------------
#Система отображения/удаления профиля
#-----------------------------------------------------------------------------------------------------------------------

@dp.message_handler(state=MenuStates.profile)
async def handle_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    if select == "👤Профиль":
        # Запрос данных пользователя из базы данных Supabase
        user = users.get(chat_id)
        pseudo = user.full_name
        gender = user.gender
        age = user.age
        balance = user.balance
        userlist = supabase.table('UsersData').select('chat_id').order('balance', desc=True).execute().data
        counter = 0
        while userlist[counter]['chat_id'] != chat_id:
            counter+=1
        if gender:
            gender = "🙋‍♂️"
            image = os.environ.get("MALE")
        else:
            gender = "🙋‍♀️"
            image = os.environ.get("FEMALE")
        # Формирование сообщения профиля пользователя
        profile_message = f"Добро пожаловать в ваш профиль:\n\n" \
                          f"{gender}{pseudo}, {age} лет\n└Ваше место в топе: {counter+1}\n\n" \
                          f"💰Баланс: {balance}🔘 поинтов\n└Мероприятий посещено: ?"
        await bot.send_photo(chat_id=chat_id, photo=image, caption=profile_message, reply_markup=profilebuttons)
    # Обработчик нажатия на кнопку удалить профиль
    elif select == "❌Удалить профиль":
        await bot.send_message(chat_id, "Вы действительно хотите удалить свой профиль?", reply_markup=confirmbutton)
        await ProlfileStates.delete_profile.set()
    elif select == "⚙️Редактировать профиль":
        await ProlfileStates.edit_profile.set()
        await bot.send_message(chat_id, "Выберите какие данные хотите отредактировать! ", reply_markup=menuedit)
    elif select == "⬅️Назад в меню":
        await MenuStates.waiting_for_profile.set()
        await bot.send_message(chat_id, "Вы вернулись в меню!", reply_markup=rkbm)
    
    else:
        await bot.send_message(chat_id, "Некорректный выбор.")
    
@dp.message_handler(state=ProlfileStates.delete_profile)
async def del_profile(message: types.Message, state: FSMContext):
    select = message.text
    chat_id = message.chat.id
    tgname = message.from_user.username
    if tgname == None and select == "❗Я действительно хочу удалить свой профиль и понимаю, что все мои данные будут удалены в том числе и баланс.":
        user = users.get(chat_id)
        users.delete(user)
        supabase.table('UsedPromocode').delete().eq('chat_id', chat_id).execute()
        supabase.table('Pointer').delete().eq('chat_id', chat_id).execute()
        await bot.send_message(chat_id, "Ваш профиль был удален!", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    elif tgname != None and select == "❗Я действительно хочу удалить свой профиль и понимаю, что все мои данные будут удалены в том числе и баланс.":
        tgname = "@" + tgname
        user = users.get(tgname)
        users.delete(user)
        supabase.table('Pointer').delete().eq('chat_id', chat_id).execute()
        supabase.table('UsedPromocode').delete().eq('chat_id', chat_id).execute()
        supabase.table('Report').delete().eq('tgusr',tgname).execute()
        await bot.send_message(chat_id, "Ваш профиль был удален!", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    elif select == "⬅️Назад в меню":
        await MenuStates.waiting_for_profile.set()
        await bot.send_message(chat_id, "Вы вернулись в меню!", reply_markup=rkbm)
    else:
        await MenuStates.waiting_for_profile.set()
        await bot.send_message(chat_id, "Некорректный выбор, вы вернулись в меню!", reply_markup=rkbm)

#-----------------------------------------------------------------------------------------------------------------------
#Система отображения мероприятий
#-----------------------------------------------------------------------------------------------------------------------
    
@dp.message_handler(state=MenuStates.calendar)
async def handle_calendar(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    response = supabase.table('Event').select('*').limit(5).execute()
    events_message = 'Мероприятия:'
    for event in response.data:
        url = 'https://leader-id.ru/events/'
        url = url +str(event['id'])
        name = event['full_name']
        date_start = event['date_start'][:16]
        date_end = event['date_end']
        date = date_start + "-" + date_end[11:16]
        print(date)
        events_message += f' \n' \
                         f"[{name}]({url}) \n" \
                         f"⏱{date} \n" \
                         f'------------------------------'
    await bot.send_message(chat_id, events_message,disable_web_page_preview=True,parse_mode=types.ParseMode.MARKDOWN)
    await MenuStates.waiting_for_profile.set()
    user = users.get(chat_id)
    user.user_state = str(MenuStates.calendar)
    
#-----------------------------------------------------------------------------------------------------------------------
#Система тикетов для юзера
#-----------------------------------------------------------------------------------------------------------------------

@dp.message_handler(state=MenuStates.help)
async def handle_help(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    await bot.send_message(chat_id, f"Привет! Если у тебя есть какие-то проблемы или пожелания , то смелее нажимай на кнопку '📨Создать заявку' и администратор с радостью тебе поможет! ", reply_markup=userhelp)
    user = users.get(chat_id)
    user.user_state = str(MenuStates.help)
    users.set(user)
    await MenuStates.help_start.set()
    user.user_state = str(MenuStates.help_start)


@dp.message_handler(text="📨Создать заявку", state=MenuStates.help_start)
async def handle_help_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    tgu = message.from_user.username
    tgus = '@' + tgu

    # Проверяем, есть ли у пользователя предыдущие заявки
    existing_reports = supabase.table('Report').select('tgusr').eq('tgusr', tgus).execute()
    if existing_reports.data:
        await message.reply("У вас уже есть открытая заявка. Пожалуйста, дождитесь ответа.", reply_markup=rkbm)
        await state.finish()
        await MenuStates.waiting_for_profile.set()

        user = users.get(chat_id)
        user.user_state = str(MenuStates.help)
        users.set(user)
        return

    await bot.send_message(chat_id, "Нажата кнопка создать заявку", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(chat_id, "Распишите здесь наиподробнейшим образом какой у вас возник вопрос или пожелание!",reply_markup=cancel_button_for_user_help)

    user = users.get(chat_id)
    user.user_state = str(MenuStates.help_end)
    await MenuStates.help_end.set()

@dp.message_handler(state=MenuStates.help_end)
async def handle_help_end(message: types.Message, state: FSMContext):
    try:
        Description = message.text
        chat_id = message.chat.id
        telegram_name = message.from_user.username
        tgusr = telegram_name
        if telegram_name == None:
            await bot.send_message(chat_id, "У вас нет имени пользователя телеграм!Укажите его в своём профиле и тогда администрация сможет вам помочь.", reply_markup=userhelp)
            await MenuStates.help_cancel.set()

        else:
            tgusr = "@" + telegram_name

        # Вставка в БД
        supabase.table('Report').insert({'description': Description, 'tgusr': tgusr}).execute()

        # Подтверждающее сообщение
        await bot.send_message(chat_id, "Заявка успешно отправлена! В ближайшее время с вами свяжется администратор.", reply_markup=userhelp)

    except:
        chat_id = message.chat.id
        await bot.send_message(chat_id, "Извините, произошла ошибка при отправке заявки", reply_markup=userhelp)
        await MenuStates.help_cancel.set()

    # Сброс состояния
    await state.finish()
    await MenuStates.help_ender.set()
    users.user_state=str(MenuStates.help)

@dp.message_handler(text = "⬅️Назад в меню", state=[MenuStates.help,MenuStates.help_start,MenuStates.help_ender,MenuStates.help_cancel])
async def handle_help_back(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await MenuStates.waiting_for_profile.set()
    await bot.send_message(chat_id, "Вы вернулись в меню!", reply_markup=rkbm)

#-----------------------------------------------------------------------------------------------------------------------
#Система тикетов для админов
#-----------------------------------------------------------------------------------------------------------------------

@dp.message_handler(text = "📨Обращения", state = AdminPanel.admin_menu)
async def handle_report(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Нажата кнопка обращений, здесь вы можете просмотреть действующие обращения от пользователей или удалить уже решённые. ", reply_markup=admreport)
    await AdminPanel.ticket.set()
    user = users.get(chat_id)
    user.user_state = str(AdminPanel.ticket)


@dp.message_handler(text='Действующие обращения', state=AdminPanel.ticket)
async def check_tickets(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = users.get(chat_id)
    user.user_state = str(AdminPanel.ticket_check)

    # Запрос обращений из БД
    tickets = supabase.table('Report').select('tgusr', 'description').execute().data

    tickets_text = "📨 Действующие обращения:\n\n"

    for i, ticket in enumerate(tickets, 1):
        username = ticket['tgusr']
        description = ticket['description']
        tickets_text += f"{i}. {username} - {description}\n"

    # Отправка сообщения
    await bot.send_message(chat_id, tickets_text)

    # Смена состояния
    await AdminPanel.ticket.set()
    user.user_state = str(AdminPanel.ticket)

@dp.message_handler(text = "Удалить обращение", state=AdminPanel.ticket)
async def delete_ticket(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await AdminPanel.ticket_delete.set()
    user = users.get(chat_id)
    user.user_state = str(AdminPanel.ticket_delete)
    await message.reply("Введите @username пользователя чтобы удалить его заявку", reply_markup=types.ReplyKeyboardRemove())
    await AdminPanel.ticket_start.set()
    user.user_state = str(AdminPanel.ticket_delete)


@dp.message_handler(state=AdminPanel.ticket_start)
async def handle_ticket_delete(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    username = message.text

    # Проверка, есть ли такой пользователь
    user_exists = supabase.table('Report').select('tgusr').eq('tgusr', username).execute()
    if not user_exists.data:
        await message.reply("Такого пользователя нет в базе данных", reply_markup= admreport)
        await state.finish()
        await AdminPanel.ticket.set()
        return

    # Удаление обращения
    delete_query = supabase.table('Report').delete().eq('tgusr', username).execute()

    await message.reply(f"Обращение пользователя {username} успешно удалено", reply_markup=admreport)
    await AdminPanel.ticket.set()
    user = users.get(chat_id)
    user.user_state = str(AdminPanel.ticket)


@dp.message_handler(text="⬅️Назад в меню", state=AdminPanel.ticket)
async def handle_tickets_back(message: types.Message, state: FSMContext):
    await message.reply("Вы вернулись в админ меню", reply_markup=admrkbm)
    await AdminPanel.admin_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.admin_menu)
    users.set(user)

#-----------------------------------------------------------------------------------------------------------------------
#Система заданий
#-----------------------------------------------------------------------------------------------------------------------

@dp.message_handler(state=MenuStates.tasks) #Вывод коллекции заданий (1 рубеж) AdminTasks
async def handle_tasks(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    counter = supabase.table('Pointer').select('counter').eq('chat_id', chat_id).execute().data[0]['counter']
    task = supabase.table('AdminTasks').select('name','description').eq('counter', counter).execute().data[0]
    text = f"{counter}.{task['name']}\n{task['description']}"
    await bot.send_photo(chat_id, "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/BoilerPoint.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L0JvaWxlclBvaW50LmpwZyIsImlhdCI6MTY5MDg4MjU1NiwiZXhwIjoxNzIyNDE4NTU2fQ.-AMp6dtQcRWE9JIV0JDR1GOMZ1ldE7LCAQxr27l2Szo&t=2023-08-01T09%3A35%3A58.287Z", text, reply_markup= ikbmtasks)

    user = users.get(chat_id)
    user.user_state = str(MenuStates.tasks)
    users.set(user)
    await MenuStates.waiting_for_profile.set()

@dp.callback_query_handler(text="right", state=MenuStates.waiting_for_profile) #кнопка вправо 1 рубеж
async def right(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    counter = supabase.table('Pointer').select('counter').eq('chat_id', chat_id).execute()
    counter = counter.data[0]['counter'] + 1
    if counter>supabase.table('AdminTasks').select('counter' ).order('counter', desc = True).limit(1).execute().data[0]['counter']:
        counter = 0
    supabase.table('Pointer').update({'counter' : counter}).eq('chat_id', chat_id).execute()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await handle_tasks(call.message, state)

@dp.callback_query_handler(text="left", state=MenuStates.waiting_for_profile) # кнопка влево 1 рубеж
async def left(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    counter = supabase.table('Pointer').select('counter').eq('chat_id', chat_id).execute()
    counter = counter.data[0]['counter'] - 1
    if counter<0:
        counter = supabase.table('AdminTasks').select('counter' ).order('counter', desc = True).limit(1).execute().data[0]['counter']
    supabase.table('Pointer').update({'counter' : counter}).eq('chat_id', chat_id).execute()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await handle_tasks(call.message, state)

@dp.callback_query_handler(text="go", state=MenuStates.waiting_for_profile) #Человек выбрал задание и перешел в выбор вопроса # переход ко 2 рубежу # отображение 2 рубежа вариантов вопросов внутри коллекции заданий
async def go(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    counter = supabase.table('Pointer').select('counter').eq('chat_id', chat_id).execute()
    counter = counter.data[0]['counter']
    counter = 0
    question_list = supabase.table('AdminQuestion').select('question' ).eq('counter', counter).order('number', desc = False).execute().data
    ikq = InlineKeyboardMarkup(row_width=1)
    for keynomber in range(len(question_list)):
        Rkey = InlineKeyboardButton(text=str(question_list[keynomber]["question"]), callback_data=keynomber)
        ikq.row(Rkey)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id, "Список заданий:", reply_markup=ikq)
    await MenuStates.waiting_for_profile.set()

@dp.callback_query_handler(text=[0,1,2,3,4,5,6,7], state=MenuStates.waiting_for_profile) #Человек выбрал вопрос, отображение вариантов ответов внутри вопроса
async def question( call: types.CallbackQuery, state: FSMContext):
    message = call.data
    chat_id = call.message.chat.id
    counter = supabase.table('Pointer').select('counter').eq('chat_id', chat_id).execute().data[0]['counter']
    counter = 0
    question_text = supabase.table('AdminQuestion').select('questionfull' ).eq('counter', counter).order('number', desc = False).execute().data[int(message)]
    answer_list = supabase.table('AdminAnswerOptions').select('answer').eq('counter', counter).execute().data
    ikanswer = InlineKeyboardMarkup(row_width=1)
    for keynomber in range(len(answer_list)):
        Rkey = InlineKeyboardButton(text=str(answer_list[keynomber]['answer']), callback_data=f'A{keynomber}')
        ikanswer.row(Rkey)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_photo(chat_id, "https://qdsibpkizystoiqpvoxo.supabase.co/storage/v1/object/sign/static/bot/BoilerPoint.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGF0aWMvYm90L0JvaWxlclBvaW50LmpwZyIsImlhdCI6MTY5MDg4MjU1NiwiZXhwIjoxNzIyNDE4NTU2fQ.-AMp6dtQcRWE9JIV0JDR1GOMZ1ldE7LCAQxr27l2Szo&t=2023-08-01T09%3A35%3A58.287Z", question_text['questionfull'], reply_markup=ikanswer)
    await MenuStates.waiting_for_profile.set()

@dp.callback_query_handler(text=["A0","A1","A2","A3",], state=MenuStates.waiting_for_profile) # выбор варианта ответа и результат
async def answer( call: types.CallbackQuery, state: FSMContext):
    message = call.data[1:]
    chat_id = call.message.chat.id
    counter = supabase.table('Pointer').select('counter').eq('chat_id', chat_id).execute().data[0]['counter']
    counter = 0
    answer = bool(supabase.table('AdminAnswerOptions').select('correct').eq('counter', counter).execute().data[int(message)]['correct'])
    if answer == True:
        await bot.send_message(chat_id, "Ответ верный")
    else:
        await bot.send_message(chat_id, "Вы ошиблись!")
    await MenuStates.waiting_for_profile.set()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
#-----------------------------------------------------------------------------------------------------------------------
#Система заданий
#-----------------------------------------------------------------------------------------------------------------------

# Ответ на отправку стикера
@dp.message_handler(content_types=types.ContentType.STICKER, state="*")
async def handle_sticker(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Извините, я не принимаю стикеры.")

# ВНИМАНИЕ! Данный handler ловит людей без состояния!
@dp.message_handler(state= None)
async def handle_The_Last_Frontier(message: types.Message, state: FSMContext):
    sost = await state.get_state()
    print(sost)
    await start_command(message, state)

#-----------------------------------------------------------------------------------------------------------------------
#Система для Telegram Web App
#-----------------------------------------------------------------------------------------------------------------------

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA, state='*')
async def handle_qr(message: types.ContentType.WEB_APP_DATA , state: FSMContext):
    message.text = message.web_app_data.data
    await asyncio.wait_for(check_promocode(message,state),timeout=3.5)

    await message.delete()

#-----------------------------------------------------------------------------------------------------------------------
#Система для Telegram Web App
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)