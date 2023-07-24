import random
import string
import os
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

# Инициализация подключения к базе данных Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

table_name = "Promocode"


def generate_code(length=16):
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    return code


def generate_promo(usages, cost):
    code = generate_code()
    print(f"Generated promo code: {code}")

    if cost == 0:
        cost = 1

    data = {
        'promo': code,
        'last': usages,
        'cost': cost
    }

    supabase.table(table_name).insert(data).execute()
    print(f"Added {code} with {usages} usages and {cost} cost to {table_name} table")
    return code

