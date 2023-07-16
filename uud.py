import uuid

def generate_uuid_from_chat_id(chatid):
    # Преобразование chat ID в строку
    chat_id_str = str(chatid)

    # Генерация UUID на основе chat ID
    generated_uuid = uuid.uuid5(uuid.NAMESPACE_OID, chat_id_str)

    return str(generated_uuid)



