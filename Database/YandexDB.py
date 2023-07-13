import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Инициализация подключение к Базе Данных Yandex Data-Base через AWS с boto3
database = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("USER_STORAGE_URL"),
    region_name='ru-central1',
    aws_access_key_id=os.getenv("AWS_PUBLIC_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
)
table = database.Table('table123')