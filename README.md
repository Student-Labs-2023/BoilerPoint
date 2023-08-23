# BoilerPoint


![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/6a43322d-326c-4fd4-aeb3-55b56d6bedb0)


## Dependencies

1. Для установки зависимостей вам необходимо запустить installer.bat или же прописать в консоли :

```sh
pip install requirements.txt
```

2. Получите все переменные для вашей среды следующим образом :

- Из документации по gspread узнайте как получить ваш credentials.json , который необходимо оставить в корневой папке и GoogleSheets

- Из документации по supabase узнайте как получить ваши SUPABASE_URL & SUPABASE_KEY

3. Теперь перейдите в @BotFather в телеграм и получите токен для вашего бота :

- Поместите токен в .env файл с параметром TOKEN 


Теперь переместите свои .env файлы в корневую директорию проекта , а также в Database



# Для тестировщиков 

- Зарегистрируйтесь в SupaBase и пришлите мне в телеграм (t.me/whitehodok) e-mail на который вы зарегистрировались
  
- Получите у меня в телеграме (t.me/whitehodok) наш .env файл
  
- Получите у меня в телеграме (t.me/whitehodok) наш credentials.json

# Для проверяющих 

- Напишите мне в телеграм https://t.me/whitehodok с просьбой скинуть последний билд бота

- Установите все необходимые зависимости через консоль, прописав следующее 

``` 
pip install -r requirements.txt
```
- Запустите main.py любым удобным для вас способом

# Схема проекта на текущий момент

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/ee14121c-6085-4e2c-9e8a-1cc66eb3a20b)

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/be27e216-883a-4f6d-9fc8-098dcdde7102)



# Схема базы данных на текущий момент

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/e40a735a-3d66-45ee-adcc-634cb45e7b86)



# Documentation 

| Frame    |   Docs                                                   |
|-----------|---------------------------------------------------------|
|SupaBase   | https://supabase.com/docs |
|gspread    | https://gspread.readthedocs.io/_/downloads/en/latest/pdf/ |
|pydantic   | https://docs.pydantic.dev/latest/ | 
|aiogram    | https://aiogram.readthedocs.io/_/downloads/en/latest/pdf/ |
|schedule   | https://schedule.readthedocs.io/en/stable/installation.html |
|qrcode     | https://pypi.org/project/qrcode/ |
|pyzbar     | https://pypi.org/project/pyzbar/ |
|userguide  | https://github.com/Student-Labs-2023/BoilerPoint/tree/main/Documentation/User%20guide |


# Start Jelezyaka 

После установки зависимостей и подключений введите в консоли следующее :

```py
py main.py
```


![pinhuin](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/23b4b9d0-494c-4b3e-8a8b-00cce18a8d90)





