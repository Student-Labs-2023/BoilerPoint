from dotenv import load_dotenv
from aiogram import Bot, types
from Database.YandexDB import table
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from boto3.dynamodb.conditions import Key
from dataclasses import dataclass
from typing import Optional
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import ikbg, rkbm,admrkbm,admin_list
from pydantic import BaseModel, Field, ValidationError, validator
from validator import ValidatedUserRegistrationDTO
from state import update_user_state

load_dotenv()

# Инициализация бота, диспетчера и хранилища состояний
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

# DTO для хранения состояния регистрации пользователей
@dataclass
class UserRegistrationDTO:
    chat_id: str
    age: Optional[str] = None
    gender: Optional[str] = None
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

class AdminStates(StatesGroup):
    adminmenu = State()


        
@dp.message_handler(Command('start'), state=None)
async def start_command(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # Проверка наличия пользователя в базе данных
    response = table.query(KeyConditionExpression=Key('chatid').eq(str(chat_id)))
    if response.get('Items'):
        # Пользователь уже зарегистрирован
        await MenuStates.waiting_for_profile.set()
        await message.reply("Чтобы просмотреть свой профиль, нажмите кнопку 'Профиль'.")
    else:
        # Регистрация нового пользователя
        user_registration[chat_id] = UserRegistrationDTO(chat_id)
        await message.reply("Привет! Давай зарегистрируемся! Введите ваш возраст:")

        # Установка состояния "waiting_for_age" для пользователя
        await RegistrationStates.waiting_for_age.set()

        # Сохранение состояния пользователя
        update_user_state(str(chat_id), str(RegistrationStates.waiting_for_age))

@dp.message_handler(state=RegistrationStates.waiting_for_age)
async def handle_age(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    age = message.text

    # Проверка и валидация возраста пользователя
    try:
        validated_age = ValidatedUserRegistrationDTO(chat_id=chat_id, age=age).age
    except ValidationError as e:
        error_msg = e.errors()[0]["msg"]
        await message.reply(error_msg)
        return

    # Сохранение возраста пользователя в DTO
    dto = user_registration[chat_id]
    dto.age = validated_age
    print(f"Возраст пользователя {chat_id}: {validated_age}")

    # Запрашиваем пол пользователя
    await message.reply("Введите ваш пол (Male/Female):", reply_markup=ikbg)

    # Переход к следующему состоянию "waiting_for_gender"
    await RegistrationStates.waiting_for_gender.set()
    # Сохранение состояния пользователя
    update_user_state(str(chat_id), str(RegistrationStates.waiting_for_gender))

@dp.callback_query_handler(state=RegistrationStates.waiting_for_gender)
async def handle_gender_callback(query: types.CallbackQuery, state: FSMContext):
    chat_id = query.message.chat.id
    gender = query.data.lower()

    # Сохранение выбранного пола в DTO
    dto = user_registration[chat_id]
    dto.gender = gender.capitalize()
    print(f"Пол пользователя {chat_id}: {gender}")

    # Запрашиваем имя пользователя
    await query.message.reply("Введите ваше ФИО:")

    # Переход к следующему состоянию "waiting_for_name"
    await RegistrationStates.waiting_for_name.set()

    # Сохранение состояния пользователя
    update_user_state(str(chat_id), str(RegistrationStates.waiting_for_name))

@dp.message_handler(state=RegistrationStates.waiting_for_name)
async def handle_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    name = message.text

    # Сохранение имени пользователя в DTO
    dto = user_registration[chat_id]
    dto.name = name
    print(f"Имя пользователя {chat_id}: {name}")

    # Получаем имя пользователя из его профиля в Telegram
    telegram_name = message.from_user.first_name

    # Обновление данных пользователя в базе данных
    try:
        tg_username = '@' + message.from_user.username if message.from_user.username else dto.name
        response = table.put_item(
            Item={
                'chatid': str(dto.chat_id),  # Тип String
                'pseudo': dto.name ,  # Тип String (Псевдоним в базе данных)
                'name': telegram_name,  # Тип String (имя в Telegram)
                'age': int(dto.age),  # Тип Number
                'gender': dto.gender,  # Тип String
                'balance': 0,  # Тип Number
                'tgusr': tg_username  # Тип String
            }
        )
        print(f"Данные пользователя {chat_id} обновлены: {response}")
    except Exception as e:
        print(f"Ошибка при обновлении данных пользователя {chat_id}: {e}")

    # Обновление состояния пользователя в базе данных
    update_user_state(str(chat_id), str(RegistrationStates.final_reg))

    # Отправка сообщения о успешной регистрации
    await bot.send_message(chat_id, f"Регистрация успешно завершена, {dto.name}!", reply_markup=rkbm)

    # Удаление данных о регистрации пользователя из словаря user_registration
    del user_registration[chat_id]
    print(f"Данные о регистрации пользователя {chat_id} удалены")
    await state.finish()
    await MenuStates.profile.set()

@dp.message_handler(state=MenuStates.waiting_for_profile)
async def handle_waiting_for_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    if select == "👤Профиль":
        await MenuStates.profile.set()
        await handle_profile(message, state)
    else:
        await message.reply("Чтобы просмотреть свой профиль, нажмите кнопку 'Профиль'.")

@dp.message_handler(state=MenuStates.profile)
async def handle_profile(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    select = message.text
    if select == "👤Профиль":
        # Запрос данных пользователя из базы данных
        update_user_state(str(chat_id), str(MenuStates.profile))
        response = table.query(KeyConditionExpression=Key('chatid').eq(str(chat_id)))
        items = response.get('Items')
        if items:
            user_data = items[0]
            pseudo = user_data.get('pseudo', 'Unknown')
            gender = user_data.get('gender', 'Unknown')
            age = user_data.get('age', 'Unknown')
            name = user_data.get('name', 'Unknown')
            balance = user_data.get('balance', 0)
            if gender in ['Male']:
                gender = "🙋‍♂️"
                image = "image.png"
            else:
                gender = "🙋‍♀️"
                image = "image.png"
            # Формирование сообщения профиля пользователя
            profile_message = f"Добро пожаловать в ваш профиль:\n\n" \
                              f"{gender}{pseudo}, {age} Лет\n├Ваш юзернейм: {name}\n└Ваше место в топе: ?\n\n" \
                              f"💰Баланс: {balance}⭐\n└Мероприятий посещено: ?"

            await bot.send_photo(chat_id=chat_id, photo=open(image, 'rb'), caption=profile_message)
        else:
            await bot.send_message(chat_id, "Профиль не найден.")
    else:
        await bot.send_message(chat_id, "Некорректный выбор.")

@dp.message_handler(Command('admin'), state=None)
async def admin_command(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if chat_id in admin_list:
        await state.finish()
        await AdminStates.adminmenu.set()
        await message.reply("Добро пожаловать в консоль администратора:", reply_markup=admrkbm)


# Ответ на отправку стикера
@dp.message_handler(content_types=types.ContentType.STICKER, state=None)
async def handle_sticker(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Извините, я не принимаю стикеры.")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)