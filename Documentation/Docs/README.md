# Техническая документация 

## Disclaimer 

Документация делается на случай того, если связь с 4-мя разрабами окончательно потеряется и нельзя будет поддерживать бота без их участия.
Вся документация пишется исключительно по доброй воле и не является 100% технической, скорее составляется на тот случай, если другого выхода не будет.


Разработчики:

1. https://github.com/WhiteHodok

2. https://github.com/Qubicool

3. https://github.com/Goldenbarnowl

4. https://github.com/dudava (Web-App)


# За что отвечает каждый импорт 

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/702df1c4-5f2c-4c57-97a4-a0348799a1a7)


## json 
- Работа с JSON файлами

## PIL.image 
- Работа с QR 

## io 
- Хранение QR кода в опреативной памяти при его создании

## pyzbar 
- Чтение QR кодов с текста

## aiogram 
- Фреймворк на котором сделан бот

## os 
- Подтягивание .env файлов в файловой системе компьютера

## buttons 
- buttons.py отвечает за кнопки в боте 

## src... 
- UserRepostiory для удобного обращения к БД 

## GoogleSheets (gspread)
- Для работы гугл-таблиц

## codegen 
- Функции для генерации промокодов

## funcs 
- Функции для работы бота

## ast
- Dependencies QR


# Finite State Machine

## Для чего нужны стейты (состояния)

- Стейты нужны для работы с клавиатурой
- При наличии стейтов нельзя попасть в админку не находясь в roles.json или создать ивент
- https://mastergroosha.github.io/aiogram-2-guide/fsm/ 

## Как объявить новое состояние 

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/292b5e4b-9b61-4166-adc5-e07401b36a74)


- Создать новый класс и передать в класс от которого он наследуется StatesGroup
- Передать аргументы нового состояния следующим образом 


```py
class RegistrationStates(StatesGroup):
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_name = State()
    final_reg = State()
```


Всё это позволит вам создать новый класс в машине состояний (FSM)


# Что делать если я вижу бота на миллион строк и не понимаю что в нём редачить 

 Определённые функции в боте можно идентифицировать однозначно с помощью следующих способов :


1. Способ 

1.1.Мы видим в нашем боте любую красивую кнопку у которой хотим изменить функционал.

1.2.Заходим в любой IDE, открываем main.py, нажимаем CTR+F и пишем текст кнопки, которую хотим изменить.

1.3.Вы прекрасны


2. Способ 

2.1. Мы знаем про существование FSM в нашем боте 

2.2. Заходим в нужный класс и делаем CTR+F по этому стейту.

2.3. Profit


3. Способ 

3.1. Весь код в боте разделён на тематические блоки :

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/d5934852-5efa-46ee-bd0a-daf4eb1f6ac7)

Эти блоки сообщают нам о том за что конкретно отвечает каждый блок

3.2. Все хендлеры в блоке идут последовательно и не разорваны по коду мейна, т.е каждая клавиатура идёт последовательно друг за другом и никак иначе.


## Структура .env

```
TOKEN = 
SUPABASE_URL = 
SUPABASE_KEY = 
MALE = 
FEMALE =
```

## Структура JSON  

```
{
  "type": "service_account",
  "project_id": "boilerpoint",
  "private_key_id": "",
  "private_key": "-----BEGIN PRIVATE KEY-----\n-----END PRIVATE KEY-----\n",
  "client_email": "",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "",
  "universe_domain": "googleapis.com"
}
```

