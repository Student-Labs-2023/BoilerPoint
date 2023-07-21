from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.utils import executor
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
from Database.DataUsers import update_user_state_by_id, delete_user_data_by_id, get_user_info_by_id, \
    update_user_fullname_by_tgusr, update_user_age_by_tgusr, update_user_balance_by_tgusr

load_dotenv()

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
    calendar = State()
    help = State()
    rating = State()

# Состояние удаления профиля
class ProlfileStates(StatesGroup):
    delete_profile = State()

# Состояния админ-панели
class AdminPanel(StatesGroup):
    admin_menu = State()
    change_user = State()
    change_user_end = State()
    change_user_start = State()
    change_user_fullname = State()
    change_user_fullnamestart = State()
    change_user_age = State()
    change_user_agestart = State()
    change_user_balance = State()
    change_user_balancestart = State()
    add_event = State()
    add_task = State()
    backward = State()
    rating_board = State()


cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")

# Хендлер отмены действия через кнопку
@dp.callback_query_handler(text="cancel", state="*")
async def cancel_action(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await state.finish()
    await call.message.answer("Действие отменено")


@dp.message_handler(commands=['admin'], state='*')
async def admin_command(message: types.Message, state: FSMContext):
    # Проверка, что пользователь в списке админов
    admin_list = ['5617565289', '415378656', '551929814', '390483228']
    if str(message.from_user.id) not in admin_list:
        await message.reply("У вас нет прав администратора!")
        return

    # Установка состояния и вывод кнопок админки
    await AdminPanel.admin_menu.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.admin_menu)
    users.set(user)
    await message.reply("Вы вошли в панель администратора", reply_markup=admrkbm)

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

@dp.message_handler(text="Изменить баланс", state="*")
async def admin_change_user_balance(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_balancestart.set()
    await message.reply("Введите @username пользователя, которого необходимо отредактировать", reply_markup=types.ReplyKeyboardRemove())
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.change_user_balancestart)
    users.set(user)

@dp.message_handler(state=AdminPanel.change_user_balancestart)
async def admin_change_user_balance_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    await state.update_data(username=username)
    await AdminPanel.change_user_balance.set()
    await message.reply("Введите новый баланс пользователя", reply_markup=InlineKeyboardMarkup().add(cancel_button))
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.change_user_balance)
    users.set(user)

@dp.message_handler(state=AdminPanel.change_user_balance)
async def admin_change_user_balance_handler(message: types.Message, state: FSMContext):
    new_balance = message.text
    data = await state.get_data()
    username = data.get("username")
    update_user_balance_by_tgusr(username, new_balance)
    #   Отправляем сообщение об успешном обновлении
    await message.reply(f"Баланс пользователя {username} успешно обновлен на {new_balance}", reply_markup=admue)
    await state.finish()
    await AdminPanel.change_user_end.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.change_user_end)
    users.set(user)

# Хендлер для смены фио через админа
@dp.message_handler(text="Изменить ФИО", state="*")
async def admin_change_user_fullname(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_fullnamestart.set()
    await message.reply("Введите @username пользователя, которого необходимо отредактировать", reply_markup=types.ReplyKeyboardRemove())
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.change_user_fullnamestart)
    users.set(user)

@dp.message_handler(state=AdminPanel.change_user_fullnamestart)
async def admin_change_user_fullname_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    await state.update_data(username=username)  # сохраняем username в данных состояния
    await AdminPanel.change_user_fullname.set()  # переходим к следующему состоянию
    await message.reply("Введите новое ФИО пользователя", reply_markup=InlineKeyboardMarkup().add(cancel_button))
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.change_user_fullname)
    users.set(user)

@dp.message_handler(state=AdminPanel.change_user_fullname)
async def admin_change_user_fullname_handler(message: types.Message, state: FSMContext):
    new_fullname = message.text  # получаем новое ФИО
    if new_fullname.replace(" ", "").isalpha() and len(new_fullname) < 40:
        data = await state.get_data()
        username = data.get("username")  # получаем сохраненный username из данных состояния
        # Обновляем ФИО пользователя
        update_user_fullname_by_tgusr(username, new_fullname)
        # Отправляем сообщение об успешном обновлении
        await message.reply(f"ФИО пользователя {username} успешно обновлено на {new_fullname}", reply_markup=admue)
        await state.finish()
        await AdminPanel.change_user_end.set()
        user = users.get(message.chat_id)
        user.user_state = str(AdminPanel.change_user_end)
        users.set(user)
    else:
        await message.reply("Неккоректное ФИО")
        await AdminPanel.change_user_fullname.set()
        user = users.get(message.chat.id)
        user.user_state = str(AdminPanel.change_user_fullname)
        users.set(user)

# Хендлер для смены возраста через админ меню
@dp.message_handler(text="Изменить возраст", state="*")
async def admin_change_user_age(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_age.set()
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.change_user_age)
    users.set(user)
    await message.reply("Введите @username пользователя, которого необходимо отредактировать", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=AdminPanel.change_user_age)
async def admin_change_user_age_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    await state.update_data(username=username)  # сохраняем username в данных состояния

    await AdminPanel.change_user_agestart.set()  # переходим к следующему состоянию
    user = users.get(message.chat.id)
    user.user_state = str(AdminPanel.change_user_agestart)
    users.set(user)

    await message.reply("Введите новый возраст пользователя", reply_markup=InlineKeyboardMarkup().add(cancel_button))

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
        # Обновляем возраст пользователя
        update_user_age_by_tgusr(username, new_age)
        # Отправляем сообщение об успешном обновлении
        await message.reply(f"Возраст пользователя {username} успешно обновлен на {new_age}", reply_markup=admue)
        await state.finish()
        await AdminPanel.change_user_end.set()
        user = users.get(message.chat.id)
        user.user_state = str(AdminPanel.change_user_end)
        users.set(user)

# Хедлер для бека в меню админа
@dp.message_handler(text="⬅️ к Админ меню", state=[AdminPanel.change_user_start, AdminPanel.change_user_end])
async def admin_backtomenu(message: types.Message, state: FSMContext):
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

@dp.message_handler(text="📊Борда", state=AdminPanel.admin_menu)
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
        await MenuStates.profile.set()
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
    elif select == "📆Календарь событий":
        await MenuStates.calendar.set()
        await handle_calendar(message, state)
    elif select == "❓Помощь":
        await MenuStates.help.set()
        await handle_help(message, state)
    elif select == "📝Задания":
        await MenuStates.tasks.set()
        await handle_tasks(message, state)
    elif select == "Удалить профиль ❌":
        await bot.send_message(chat_id, "Вы действительно хотите удалить свой профиль?", reply_markup=confirmbutton)
    elif select == "Я действительно хочу удалить свой профиль и понимаю, что все мои данные будут удалены в том числе и баланс.":
        await ProlfileStates.delete_profile.set()
        await del_profile(message, state)
    elif select == "Назад в меню":
        await MenuStates.waiting_for_profile.set()
        await bot.send_message(chat_id, "Вы вышли в меню! ", reply_markup=rkbm)
    elif select == "Назад в меню":
        await MenuStates.waiting_for_profile.set()
        await bot.send_message(chat_id, "Вы вышли в меню! ", reply_markup=rkbm)
    else:
        await message.reply("Нет такого варианта выбора!")

@dp.message_handler(text ="📊Рейтинг", state=MenuStates.waiting_for_profile)
async def user_rating_board(message: types.Message, state: FSMContext):
    await MenuStates.rating.set()
    user = users.get(message.chat.id)
    user.user_state = str(MenuStates.rating.set())
    users.set(user)
    await show_user_rating(message.chat.id)
    await MenuStates.waiting_for_profile.set()
    user = users.get(message.chat.id)
    user.user_state = str(MenuStates.waiting_for_profile)
    users.set(user)

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
        if gender:
            gender = "🙋‍♂️"
            image = os.environ.get("MALE")
        else:
            gender = "🙋‍♀️"
            image = os.environ.get("FEMALE")
        # Формирование сообщения профиля пользователя
        profile_message = f"Добро пожаловать в ваш профиль:\n\n" \
                          f"{gender}{pseudo}, {age} лет\n└Ваше место в топе: ?\n\n" \
                          f"💰Баланс: {balance}🔘 поинтов\n└Мероприятий посещено: ?"

        await bot.send_photo(chat_id=chat_id, photo=image, caption=profile_message, reply_markup=profilebuttons)
    else:
        await bot.send_message(chat_id, "Некорректный выбор.")
    await MenuStates.waiting_for_profile.set()

# Обработчик нажатия на кнопку удалить профиль
@dp.message_handler(state=ProlfileStates.delete_profile)
async def del_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = users.get(chat_id)
    users.delete(user)
    await bot.send_message(chat_id, "Ваш профиль был удален!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(state=MenuStates.calendar)
async def handle_calendar(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    await bot.send_message(chat_id, f"Нажата кнопка календарь")
    user = users.get(chat_id)
    user.user_state = str(MenuStates.calendar)
    users.set(user)
    await MenuStates.waiting_for_profile.set()

@dp.message_handler(state=MenuStates.help)
async def handle_help(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    await bot.send_message(chat_id, f"Привет! \n Наши разработчики размышляют над тем, что сюда написать. \n Мы находимся в раздумьях над нашей системой геймификации. \n Очень скоро тут что-то появится ! \n Если тебе есть что предложить, \n то мы ждём тебя с твоим предложением в чате Studen Labs ! ")
    user = users.get(chat_id)
    user.user_state = str(MenuStates.help)
    users.set(user)
    await MenuStates.waiting_for_profile.set()

@dp.message_handler(state=MenuStates.tasks)
async def handle_tasks(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    await bot.send_message(chat_id, f"Нажата кнопка задания")
    user = users.get(chat_id)
    user.user_state = str(MenuStates.tasks)
    users.set(user)
    await MenuStates.waiting_for_profile.set()

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

async def show_rating(chat_id: int):
    # Запрос топ 4 пользователей из БД
    top_users = supabase.table('UsersData').select('full_name', 'balance', 'tgusr').order('balance', desc = True).execute()

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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)