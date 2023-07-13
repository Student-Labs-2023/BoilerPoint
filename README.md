# BoilerPoint


![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/6a43322d-326c-4fd4-aeb3-55b56d6bedb0)


## Dependencies

1. Для установки зависимостей вам необходимо запустить installreq.bat или же прописать в консоли :

```sh
pip install requirements.txt
```


2. Необходимо установить со сторонних сайтов :

- MongoDB Server : https://www.mongodb.com/try/download/community


3. Необходимо зарегистрироваться и настроить Yandex DB :

- https://console.cloud.yandex.ru/ 
- Создайте и подключите платёжный аккаунт 


Перейдите сюда и настройте сервисный аккаунт 

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/1889abaa-e22a-42da-af14-dd1e29962d97)


![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/b31261bd-4177-4e15-bd80-e3df821a89b2)


Настройте сервисный аккаунт с указанными параметрами :

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/b0049a26-cb80-4a4b-a2d6-12c7ccc2f513)


Создайте вашу Yandex Data Base , вернувшись в дашборд каталога: 

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/e91d0ed8-c77d-485e-993a-ad9116eab0b2)


![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/88980491-1070-484e-95c1-4828fce0339b)


![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/2a9df91d-7675-4ff0-8ed1-63d7d467b987)


Перейдите в вашу БД и скопируйте этот эндпоинт (создайте .env файл и передайте это в параметр USER_STORAGE_URL):

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/ce0236c7-4890-4eef-9c7d-f294031e5971)


Вернитесь в ваш сервисный аккаунт и проделайте следующий шаг :

![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/88b4b03c-31ac-41d1-9e7a-a7cbdd67a193)


![image](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/de1074f4-2f22-4704-91a3-24253f8fea60)


Скопируйте ключи и поместите Public в своём .env в параметр AWS_PUBLIC_KEY (он короче) , а Private в AWS_SECRET_KEY (он длиннее)



Теперь перейдите в @BotFather в телеграм и получите токен для вашего бота :

- Поместите токен в .env файл с параметром TOKEN 


Теперь переместите свои .env файлы в корневую директорию проекта , а также в Database


# Documentation 
YDB - https://ydb.tech/ru/docs/
MongoDB - https://www.mongodb.com/docs/
pydantic - https://docs.pydantic.dev/latest/
aiogram - https://aiogram.readthedocs.io/_/downloads/en/latest/pdf/



# Запуск бота 

После установки зависимостей и подключений введите в консоли следующее :

```py
py main.py
```


![pinhuin](https://github.com/Student-Labs-2023/BoilerPoint/assets/39564937/23b4b9d0-494c-4b3e-8a8b-00cce18a8d90)





