from pymongo import MongoClient

# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных
db = client['FSM']

# Выбор коллекции
collection = db['FSMDB']

# Создание индекса по полю 'chatid' для обеспечения уникальности значений
collection.create_index('chatid', unique=True)


def update_user_state(chat_id: str, state: str) -> None:
    try:
        # Обновление состояния пользователя в коллекции
        collection.update_one({'chatid': chat_id}, {'$set': {'user_state': state}}, upsert=True)
        print(f"User state updated for {chat_id}")
    except Exception as e:
        print(f"Error updating user state for {chat_id}: {e}")


def get_user_state(chat_id: str) -> str:
    try:
        # Получение состояния пользователя из коллекции
        document = collection.find_one({'chatid': chat_id})
        if document:
            user_state = document['user_state']
            print(f"Retrieved user state for {chat_id}: {user_state}")
            return user_state
        else:
            return ""
    except Exception as e:
        print(f"Error retrieving user state for {chat_id}: {e}")
        return ""


# Закрытие подключения к базе данных
def close_connection():
    client.close()
