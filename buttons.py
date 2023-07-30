from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
#gender buttons
ikbg = InlineKeyboardMarkup(row_width=2)
ibm = InlineKeyboardButton(text="🙋‍♂️Мужчина",callback_data='1')
ibf = InlineKeyboardButton(text="🙋‍♀️Женщина",callback_data='0')
ikbg.add(ibm,ibf)

#menu buttons
rkbm =  ReplyKeyboardMarkup(resize_keyboard=True)
kprofile= KeyboardButton(text="👤Профиль")
kliderboard= KeyboardButton(text="📊Рейтинг")
kschedule= KeyboardButton(text="📆Календарь событий")
khelp= KeyboardButton(text="❓Помощь")
kexercise= KeyboardButton(text="📝Задания")
kpromo = KeyboardButton(text="🗝️Ввести промокод")
rkbm.row(kprofile,kexercise)
rkbm.add(kschedule)
rkbm.row(khelp,kliderboard)
rkbm.add(kpromo)

#profilemenu buttons
profilebuttons = ReplyKeyboardMarkup(resize_keyboard=True)
delprofile = KeyboardButton(text="❌Удалить профиль")
profilebuttons.row(delprofile)
editbutton = ReplyKeyboardMarkup(resize_keyboard=True)
edbutton = KeyboardButton(text="⚙️Редактировать профиль")
profilebuttons.row(edbutton)
backtomenubutton = KeyboardButton(text="⬅️Назад в меню")
profilebuttons.row(backtomenubutton)
#confirm delete button and edit button + back button to profile
back = ReplyKeyboardMarkup(resize_keyboard=True)
backbutt = KeyboardButton(text="⬅️Назад в меню")
back.row(backbutt)

menuedit = ReplyKeyboardMarkup(resize_keyboard=True)
editname = KeyboardButton(text="Изменить ФИО")
editage = KeyboardButton(text="Изменить возраст")
menuedit.row(editname)
menuedit.row(editage)
menuedit.row(backbutt)

confirmbutton = ReplyKeyboardMarkup(resize_keyboard=True)
confbutton = KeyboardButton(text="❗Я действительно хочу удалить свой профиль и понимаю, что все мои данные будут удалены в том числе и баланс.")
backbutton = KeyboardButton(text="⬅️Назад в меню")
confirmbutton.row(confbutton)
confirmbutton.row(backbutton)

#usermaker buttons
usermakerkbm = ReplyKeyboardMarkup(resize_keyboard=True)
usmkbm_task = KeyboardButton(text="📝Создать задание")
usmkbm_menu = KeyboardButton(text="⬅️Меню")
usermakerkbm.row(usmkbm_task)
usermakerkbm.row(usmkbm_menu)


#admin buttons
admrkbm = ReplyKeyboardMarkup(resize_keyboard=True)
admk_user_editor = KeyboardButton(text="⚙️Изменить пользователя")
admk_event_creation = KeyboardButton(text="🛠️Создать мероприятие")
admk_job_creation = KeyboardButton(text="📝Создать задание")
admk_menu = KeyboardButton(text="⬅️Меню")
admk_liderboard = KeyboardButton(text="📊Рейтинг")
admk_promo = KeyboardButton(text="🗝️Промокоды")
admk_ticket = KeyboardButton(text="Обращения")
admk_rules = KeyboardButton(text="Права")
admrkbm.row(admk_user_editor,admk_event_creation)
admrkbm.row(admk_job_creation,admk_promo)
admrkbm.row(admk_ticket,admk_liderboard)
admrkbm.row(admk_menu,admk_rules)

#rules keyboard
ruleskbm = ReplyKeyboardMarkup(resize_keyboard=True)
ruleskbm_addmaker = KeyboardButton(text="Выдать права")
ruleskbm_delmaker = KeyboardButton(text="Забрать права")
ruleskbm_check = KeyboardButton(text="Действующие права")
ruleskbm_back = KeyboardButton(text="⬅️Админ меню")
ruleskbm.row(ruleskbm_addmaker,ruleskbm_delmaker)
ruleskbm.row(ruleskbm_check)
ruleskbm.row(ruleskbm_back)

# admin report keyboard
admreport = ReplyKeyboardMarkup(resize_keyboard=True)
admreport_check = KeyboardButton(text="Действующие обращения")
admreport_del = KeyboardButton(text="Удалить обращение")
admreport_back = KeyboardButton(text="⬅️Назад в меню")
admreport.row(admreport_check)
admreport.row(admreport_del)
admreport.row(admreport_back)

#User help button
userhelp = ReplyKeyboardMarkup(resize_keyboard=True)
userhelp_back = KeyboardButton(text="⬅️Назад в меню")
userhelp_ticket = KeyboardButton(text="📨Создать заявку")
userhelp.row(userhelp_ticket)
userhelp.row(userhelp_back)

# admin user editor button
admue = ReplyKeyboardMarkup(resize_keyboard=True)
admue_fullname_editor = KeyboardButton(text="Изменить ФИО")
admue_age_editor = KeyboardButton(text="Изменить возраст")
admue_balance_editor = KeyboardButton(text="Изменить баланс")
admue_get_info_user = KeyboardButton(text="Получить информацию о пользователе")
admue_back = KeyboardButton(text="⬅️Админ меню")
admue.row(admue_get_info_user)
admue.row(admue_fullname_editor,admue_age_editor,admue_balance_editor)
admue.row(admue_back)
admui = ReplyKeyboardMarkup(resize_keyboard=True)
admui_back = InlineKeyboardButton(text="⬅️Отменить редактирование")

#admin promo button
admpromo = ReplyKeyboardMarkup(resize_keyboard=True)
admpromo_checkpromo = KeyboardButton(text="Действующие промокоды")
admpromo_addpromo = KeyboardButton(text="Добавить промокод")
admpromo_namingpromo = KeyboardButton(text="Нэйминг-промо")
admpromo_delpromo = KeyboardButton(text="Удалить промокод")
addpromo_addqr = KeyboardButton(text="Добавить QR")
admpromo.row(addpromo_addqr)
admpromo.row(admpromo_checkpromo)
admpromo.row(admpromo_addpromo,admpromo_namingpromo,admpromo_delpromo)
admpromo.row(admue_back)

cancel_button = InlineKeyboardButton(text="❌Отмена", callback_data="cancel")

# Отмена редактирования для юзера
cancel_button_for_user = InlineKeyboardMarkup(row_width=1)
cancel_abob = InlineKeyboardButton(text="Отмена❌", callback_data="cancel_user")
cancel_button_for_user.add(cancel_abob)

cancel_button_for_user_help = InlineKeyboardMarkup(row_width=1)
cancel_helper = InlineKeyboardButton(text="Отмена❌", callback_data="cancel_user_help")
cancel_button_for_user_help.add(cancel_helper)

#task buttons
ikbmtasks = InlineKeyboardMarkup(resize_keyboard=True)
ibleft = InlineKeyboardButton(text="⬅️", callback_data="left")
ibright = InlineKeyboardButton(text="➡️", callback_data="right")
ibgo = InlineKeyboardButton(text="✅", callback_data="go")
ikbmtasks.row(ibleft,ibgo,ibright)

#rating buttons
ikbmrating = InlineKeyboardMarkup(row_width=1)
ibrating = InlineKeyboardButton(text="📊Полный рейтинг",url='https://docs.google.com/spreadsheets/d/e/2PACX-1vQFzN5HRvQhS5j4kDcv9wWH3uucCqp1AFmu2ErZYikmmJSshj1f16v7ry013vde0y6OYVWeSsVtgaKT/pubhtml?gid=0&single=true')
ikbmrating.add(ibrating)