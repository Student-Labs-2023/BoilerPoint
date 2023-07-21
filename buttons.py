from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

#remove keyboard
remover = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text = " "))


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

#profilemenu buttons
profilebuttons = ReplyKeyboardMarkup(resize_keyboard=True)
delprofile = KeyboardButton(text="Удалить профиль ❌")
profilebuttons.row(delprofile)
backtomenubutton = KeyboardButton(text="Назад в меню")
profilebuttons.row(backtomenubutton)

#confirm delete button and back button to profile
confirmbutton = ReplyKeyboardMarkup(resize_keyboard=True)
confbutton = KeyboardButton(text="Я действительно хочу удалить свой профиль и понимаю, что все мои данные будут удалены в том числе и баланс.")
backbutton = KeyboardButton(text="Назад в меню")

confirmbutton.row(confbutton)
confirmbutton.row(backbutton)


#admin buttons
admrkbm = ReplyKeyboardMarkup(resize_keyboard=True)
admk_user_editor = KeyboardButton(text="⚙️Изменить пользователя")
admk_event_creation = KeyboardButton(text="🛠️Создать мероприятие")
admk_job_creation = KeyboardButton(text="📝Создать задание")
admk_menu = KeyboardButton(text="⬅️Меню")
admk_liderboard = KeyboardButton(text="📊Борда")
admrkbm.row(admk_user_editor)
admrkbm.row(admk_event_creation)
admrkbm.row(admk_job_creation)
admrkbm.row(admk_menu,admk_liderboard)

# admin user editor button
admue = ReplyKeyboardMarkup(resize_keyboard=True)
admue_fullname_editor = KeyboardButton(text="Изменить ФИО")
admue_age_editor = KeyboardButton(text="Изменить возраст")
admue_balance_editor = KeyboardButton(text="Изменить баланс")
admue_back = KeyboardButton(text="⬅️ к Админ меню")
admue.row(admue_fullname_editor)
admue.row(admue_age_editor)
admue.row(admue_balance_editor)
admue.row(admue_back)
admui = ReplyKeyboardMarkup(resize_keyboard=True)
admui_back = InlineKeyboardButton(text="Отменить редактирование")


#rating buttons
ikbmrating = InlineKeyboardMarkup(row_width=1)
ibrating = InlineKeyboardButton(text="Полный рейтинг",url='https://docs.google.com/spreadsheets/d/e/2PACX-1vQFzN5HRvQhS5j4kDcv9wWH3uucCqp1AFmu2ErZYikmmJSshj1f16v7ry013vde0y6OYVWeSsVtgaKT/pubhtml?gid=0&single=true')
ikbmrating.add(ibrating)
