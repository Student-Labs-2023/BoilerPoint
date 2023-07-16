from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
#gender buttons

ikbg = InlineKeyboardMarkup(row_width=2)
ibm = InlineKeyboardButton(text="Мужчина",callback_data='1')
ibf = InlineKeyboardButton(text="Женщина",callback_data='0')
ikbg.add(ibm,ibf)

#menu buttons
rkbm =  ReplyKeyboardMarkup(resize_keyboard=True)
kprofile= KeyboardButton(text="👤Профиль")
kliderboard= KeyboardButton(text="📊Рейтинг")
kschedule= KeyboardButton(text="📆Календарь событий")
khelp= KeyboardButton(text="❓Помощь")
kexercise= KeyboardButton(text="📝Задания")
rkbm.row(kprofile,kexercise)
rkbm.add(kschedule)
rkbm.row(khelp,kliderboard)

#admin buttons
admin_list=['5617565289']
admrkbm = ReplyKeyboardMarkup(resize_keyboard=True)
admk_user_editor = KeyboardButton(text="⚙️Изменить пользователя")
admk_event_creation = KeyboardButton(text="🛠️Создать мероприятие")
admk_job_creation = KeyboardButton(text="📝Создать задание")
admk_menu = KeyboardButton(text="⬅️Меню")
admk_liderboard = KeyboardButton(text="📊Рейтинг")
admrkbm.row(admk_user_editor)
admrkbm.row(admk_event_creation)
admrkbm.row(admk_job_creation)
admrkbm.row(admk_menu,admk_liderboard)