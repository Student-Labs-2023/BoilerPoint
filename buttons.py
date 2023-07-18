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

#rating buttons
ikbmrating = InlineKeyboardMarkup(row_width=1)
ibrating = InlineKeyboardButton(text="Полный рейтинг",url='https://docs.google.com/spreadsheets/d/e/2PACX-1vQFzN5HRvQhS5j4kDcv9wWH3uucCqp1AFmu2ErZYikmmJSshj1f16v7ry013vde0y6OYVWeSsVtgaKT/pubhtml?gid=0&single=true')
ikbmrating.add(ibrating)