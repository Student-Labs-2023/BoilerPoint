from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dataclasses import dataclass
from typing import Optional
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import *
from Database.DataUsers import get_user_state_by_id, update_user_state_by_id, supabase,delete_user_data_by_id, get_user_info_by_id , update_user_fullname_by_tgusr, update_user_age_by_tgusr, update_user_balance_by_tgusr
from GoogleSheets.Google_sheets import rating_update_start_thread

load_dotenv()

# Инициализация бота, диспетчера и хранилища состояний
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
rating_update_start_thread()
# DTO для хранения состояния регистрации пользователей
@dataclass
class UserRegistrationDTO:
    chat_id: int
    age: Optional[int] = None
    gender: Optional[bool] = None
    name: Optional[str] = None

# Словарь для хранения экземпляров DTO
user_registration = {}

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

#Состояние удаления профиля
class ProlfileStates(StatesGroup):
    delete_profile = State()

#Состояния админ-панели
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

# Хендлер для команды /admin
@dp.message_handler(commands=['admin'], state='*')
async def admin_command(message: types.Message, state: FSMContext):

    # Проверка, что пользователь в списке админов
    admin_list = ['5617565289', '415378656']
    if str(message.from_user.id) not in admin_list:
        await message.reply("У вас нет прав администратора!")
        return

    # Установка состояния и вывод кнопок админки
    await AdminPanel.admin_menu.set()
    update_user_state_by_id(message.chat.id, str(AdminPanel.admin_menu))
    await message.reply("Вы вошли в панель администратора", reply_markup=admrkbm)

# Хендлер для кнопки  ️Изменить пользователя
@dp.message_handler(text="⚙️Изменить пользователя", state=AdminPanel.admin_menu)
async def admin_change_user(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_start.set()
    update_user_state_by_id(message.chat.id, str(AdminPanel.change_user_start))
    await message.reply("Вы попали в меню редактирования пользователя, нажмите нужную вам кнопку чтобы изменить параметры пользователя. После нажатия на кнопку введите @username человека в телеграм чтобы поменять его параметры.", reply_markup=admue)

#Хендлер для смены баланса через админа
@dp.message_handler(text="Изменить баланс", state="*")
async def admin_change_user_balance(message:types.Message, state: FSMContext):
    await AdminPanel.change_user_balancestart.set()
    await message.reply("Введите @username пользователя, которого необходимо отредактировать")

@dp.message_handler(state=AdminPanel.change_user_balancestart)
async def admin_change_user_balance_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    await state.update_data(username=username)
    await AdminPanel.change_user_balance.set()
    await message.reply("Введите новый баланс пользователя")

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
    update_user_state_by_id(message.chat.id, str(AdminPanel.change_user_end))

#Хендлер для смены фио через админа
@dp.message_handler(text="Изменить ФИО", state="*")
async def admin_change_user_fullname(message: types.Message, state: FSMContext):
    await AdminPanel.change_user_fullnamestart.set()
    await message.reply("Введите @username пользователя, которого необходимо отредактировать")

@dp.message_handler(state=AdminPanel.change_user_fullnamestart)
async def admin_change_user_fullname_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    await state.update_data(username=username)  # сохраняем username в данных состояния

    await AdminPanel.change_user_fullname.set()  # переходим к следующему состоянию
    await message.reply("Введите новое ФИО пользователя")

@dp.message_handler(state=AdminPanel.change_user_fullname)
async def admin_change_user_fullname_handler(message: types.Message, state: FSMContext):
    new_fullname = message.text  # получаем новое ФИО
    data = await state.get_data()
    username = data.get("username")  # получаем сохраненный username из данных состояния

    # Обновляем ФИО пользователя
    update_user_fullname_by_tgusr(username, new_fullname)

    # Отправляем сообщение об успешном обновлении
    await message.reply(f"ФИО пользователя {username} успешно обновлено на {new_fullname}", reply_markup=admue)
    await state.finish()
    await AdminPanel.change_user_end.set()
    update_user_state_by_id(message.chat.id, str(AdminPanel.change_user_end))

# Хендлер для смены возраста через админ меню
@dp.message_handler(text="Изменить возраст", state = "*")
async def admin_change_user_age(message: types.Message,state: FSMContext):
    await AdminPanel.change_user_age.set()
    update_user_state_by_id(message.chat.id, str(AdminPanel.change_user_age))
    await message.reply("Введите @username пользователя, которого необходимо отредактировать")

@dp.message_handler(state=AdminPanel.change_user_age)
async def admin_change_user_age_handler(message: types.Message, state: FSMContext):
    username = message.text  # получаем username
    await state.update_data(username=username)  # сохраняем username в данных состояния

    await AdminPanel.change_user_agestart.set()  # переходим к следующему состоянию
    await message.reply("Введите новый возраст пользователя")

@dp.message_handler(state=AdminPanel.change_user_agestart)
async def admin_change_user_age_handler(message: types.Message, state: FSMContext):
    new_age = message.text  # получаем новый возраст
    data = await state.get_data()
    username = data.get("username")  # получаем сохраненный username из данных состояния

    # Обновляем возраст пользователя
    update_user_age_by_tgusr(username, new_age)

    # Отправляем сообщение об успешном обновлении
    await message.reply(f"Возраст пользователя {username} успешно обновлен на {new_age}", reply_markup=admue)
    await state.finish()
    await AdminPanel.change_user_end.set()
    update_user_state_by_id(message.chat.id, str(AdminPanel.change_user_end))

# Хедлер для бека в меню админа
@dp.message_handler(text="⬅️ к Админ меню", state = [AdminPanel.change_user_start ,AdminPanel.change_user_end])
async def admin_backtomenu(message: types.Message, state: FSMContext):
    await message.reply("Вы вернулись в админ меню", reply_markup=admrkbm)
    await AdminPanel.admin_menu.set()
    update_user_state_by_id(message.chat.id, str(AdminPanel.admin_menu))

@dp.message_handler(text="⬅️Меню", state=AdminPanel.admin_menu)
async def admin_menu_back(message: types.Message, state: FSMContext):
    await MenuStates.waiting_for_profile.set()
    update_user_state_by_id(message.chat.id, str(MenuStates.waiting_for_profile))
    await message.reply("Вы вышли из панели администратора", reply_markup=rkbm)

@dp.message_handler(text="📊Борда", state=AdminPanel.admin_menu)
async def admin_rating_board(message: types.Message, state: FSMContext):
    await AdminPanel.rating_board.set()
    update_user_state_by_id(message.chat.id, str(AdminPanel.rating_board))
    await show_rating(message.chat.id)
    await AdminPanel.admin_menu.set()


@dp.message_handler(Command('start'), state=None)
async def start_command(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_state = get_user_state_by_id(chat_id)  # Получение состояния пользователя из Supabase

    if user_state:
        # Пользователь уже зарегистрирован
        await MenuStates.waiting_for_profile.set()
        await message.reply("Чтобы просмотреть свой профиль, нажмите кнопку 'Профиль'.",reply_markup=rkbm)
    else:
        # Регистрация нового пользователя
        user_registration[chat_id] = UserRegistrationDTO(chat_id)
        await message.reply("Привет! Давай зарегистрируемся! Введите ваш возраст:")

        # Установка состояния "waiting_for_age" для пользователя
        await RegistrationStates.waiting_for_age.set()
        # Сохранение состояния пользователя
        update_user_state_by_id(chat_id, str(RegistrationStates.waiting_for_age))

@dp.message_handler(state=RegistrationStates.waiting_for_age)
async def handle_age(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    age = message.text
    # Проверка и валидация возраста пользователя
    try:
        age = int(age)
    except ValueError as e:
        await bot.send_message(chat_id,"Ваш возраст неккоректен. Возраст не должен содержать буквы!")
        print(f"Error validation age{e}")
    if int(age) < 12 or int(age) > 122:
        await bot.send_message(chat_id,"Ваш возраст неккоректен. Возраст должен лежать в диапазоне от 12 - 122")
        await RegistrationStates.waiting_for_age.set()
    else:
        # Сохранение возраста пользователя в DTO
        dto = user_registration[chat_id]
        dto.age = age
        print(f"Возраст пользователя {chat_id}: {age}")

        # Запрашиваем пол пользователя
        await message.reply("Введите ваш пол (Male/Female):", reply_markup=ikbg)

        # Переход к следующему состоянию "waiting_for_gender"
        await RegistrationStates.waiting_for_gender.set()
        # Сохранение состояния пользователя
        update_user_state_by_id(chat_id, str(RegistrationStates.waiting_for_gender))

@dp.callback_query_handler(state=RegistrationStates.waiting_for_gender)
async def handle_gender_callback(query: types.CallbackQuery, state: FSMContext):
    chat_id = query.message.chat.id
    gender = query.data.lower()

    # Сохранение выбранного пола в DTO
    dto = user_registration[chat_id]
    dto.gender = bool(int(gender))
    print(f"Пол пользователя {chat_id}: {gender}")

    # Запрашиваем имя пользователя
    await query.message.reply("Введите ваше ФИО:")

    # Переход к следующему состоянию "waiting_for_name"
    await RegistrationStates.waiting_for_name.set()

    # Сохранение состояния пользователя
    update_user_state_by_id(chat_id, str(RegistrationStates.waiting_for_name))

@dp.message_handler(state=RegistrationStates.waiting_for_name)
async def handle_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    name = message.text
    
    if name.replace(" ", "").isalpha() and len(name) < 40:       
        # Сохранение имени пользователя в DTO
        dto = user_registration[chat_id]
        dto.name = name
        print(f"Имя пользователя {chat_id}: {name}")

        # Получаем имя пользователя из его профиля в Telegram
        telegram_name = message.from_user.first_name

        # Обновление данных пользователя в базе данных
        try:
            tg_username = '@' + message.from_user.username if message.from_user.username else dto.name
            response = supabase.table('UsersData').insert([{
                'full_name': dto.name,
                'chat_id': chat_id,
                'age': int(dto.age),
                'gender': bool(dto.gender),
                'user_state': str(RegistrationStates.final_reg),
                'tgusr': '@' + str(message.from_user.username)
            }]).execute()
            print(f"Данные пользователя {chat_id} обновлены: {response}")
        except Exception as e:
            print(f"Ошибка при обновлении данных пользователя {chat_id}: {e}")

        # Обновление состояния пользователя в базе данных
        update_user_state_by_id(chat_id, str(RegistrationStates.final_reg))
    
        # Отправка сообщения о успешной регистрации
        if str(message.from_user.username) == 'None':
            await bot.send_message(chat_id, f"Регистрация успешно завершена с неточностями, {dto.name}!У вас нет имени пользователя Телеграм, связь администрации с вами может быть усложнена, вам необходимо указать в вашем профиле телеграма ваше имя пользователя и перерегистрироваться в боте.", reply_markup=rkbm)
        else:
            await bot.send_message(chat_id, f"Регистрация успешно завершена, {dto.name}!", reply_markup=rkbm)
        # Удаление данных о регистрации пользователя из словаря user_registration
        del user_registration[chat_id]
        print(f"Данные о регистрации пользователя {chat_id} удалены")
        await state.finish()
        await MenuStates.profile.set()
    else:
        await bot.send_message(chat_id, f"Пожалуйста, введите корректно свое ФИО")
        await RegistrationStates.waiting_for_name.set()
#обработчик различных кнопок
@dp.message_handler(state=MenuStates.waiting_for_profile)
async def handle_waiting_for_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    if select == "👤Профиль":
        await MenuStates.profile.set()
        await handle_profile(message, state)
    elif select == "📊Рейтинг":
        await MenuStates.rating.set()
        await handle_rating(message, state)
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
    elif select == "Назад к профилю":
        await MenuStates.profile.set()
        await handle_profile(message, state)
    elif select == "Назад в меню":
        await MenuStates.waiting_for_profile.set()
        await bot.send_message(chat_id,"Вы вышли в меню! ",reply_markup=rkbm)
    else:
        await message.reply("Нет такого варианта выбора!")

#Обработчик нажатия на кнопку Профиль
@dp.message_handler(state=MenuStates.profile)
async def handle_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    if select == "👤Профиль" or select == "Назад к профилю":
        # Запрос данных пользователя из базы данных Supabase
        response = get_user_info_by_id(chat_id)
        print(response)
        items = response.data
        if len(items) > 0:
            user_data = items[0]
            pseudo = user_data.get('full_name', 'Unknown')
            gender = user_data.get('gender', 'Unknown')
            age = user_data.get('age', 'Unknown')
            balance = user_data.get('balance', 0)
            if gender:
                gender = "🙋‍♂️"
                image = os.environ.get("MALE")
            else:
                gender = "🙋‍♀️"
                image = os.environ.get("MALE")
            # Формирование сообщения профиля пользователя
            profile_message = f"Добро пожаловать в ваш профиль:\n\n" \
                              f"{gender}{pseudo}, {age} лет\n└Ваше место в топе: ?\n\n" \
                              f"💰Баланс: {balance}🔘 поинтов\n└Мероприятий посещено: ?"

            await bot.send_photo(chat_id=chat_id, photo=image, caption=profile_message, reply_markup=profilebuttons)
        else:
            await bot.send_message(chat_id, "Профиль не найден.")
    else:
        await bot.send_message(chat_id, "Некорректный выбор.")
    await MenuStates.waiting_for_profile.set()

#Обработчик нажатия на кнопку удалить профиль
@dp.message_handler(state=ProlfileStates.delete_profile)
async def del_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    delete_user_data_by_id(chat_id)
    await bot.send_message(chat_id,"Ваш профиль был удален!",reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


#Обработчик нажатия на кнопку рейтинг
@dp.message_handler(state=MenuStates.rating)
async def handle_rating(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    await bot.send_message(chat_id, f"Нажата кнопка рейтинг",reply_markup=ikbmrating)
    update_user_state_by_id(chat_id, str(MenuStates.rating))
    await MenuStates.waiting_for_profile.set()

#Обработчик нажатия на кнопку календарь
@dp.message_handler(state=MenuStates.calendar)
async def handle_calendar(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    await bot.send_message(chat_id, f"Нажата кнопка календарь")
    update_user_state_by_id(chat_id, str(MenuStates.calendar))
    await MenuStates.waiting_for_profile.set()

#Обработчик нажатия на кнопку помощь
@dp.message_handler(state=MenuStates.help)
async def handle_help(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    await bot.send_message(chat_id, f"Нажата кнопка помощь")
    update_user_state_by_id(chat_id, str(MenuStates.help))
    await MenuStates.waiting_for_profile.set()

#Обработчик нажатия на кнопку задания
@dp.message_handler(state=MenuStates.tasks)
async def handle_tasks(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    await bot.send_message(chat_id, f"Нажата кнопка задания")
    update_user_state_by_id(chat_id, str(MenuStates.tasks))
    await MenuStates.waiting_for_profile.set()


# Ответ на отправку стикера
@dp.message_handler(content_types=types.ContentType.STICKER, state=None)
async def handle_sticker(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Извините, я не принимаю стикеры.")

# ВНИМАНИЕ! Данный handler ловит людей без состояния!
@dp.message_handler(state=None)
async def handle_The_Last_Frontier(message: types.Message, state: FSMContext):
    sost = await state.get_state()
    print(sost)
    await start_command(message,state)

async def show_rating(chat_id: int):
    # Запрос топ 4 пользователей из БД
    top_users = supabase.table('UsersData').select('full_name', 'balance', 'tgusr').order('balance').limit(4).execute()

    # Формируем текст рейтинга
    rating_text = "🏆 Рейтинг пользователей 🏆\n\n"
    for i, user in enumerate(top_users.data):
        position = len(top_users.data) - i
        full_name = user['full_name']
        balance = user['balance']
        tgusr = user['tgusr']
        rating_text += f"{position}. {full_name} ({tgusr}) - {balance} баллов\n"

    # Отправляем сообщение
    await bot.send_message(chat_id, rating_text, reply_markup=ikbmrating)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

