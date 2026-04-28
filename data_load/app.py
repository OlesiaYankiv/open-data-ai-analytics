import pandas as pd
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

RAW_DATA_PATH = "/app/data/raw/glm_all_2024_portal.csv"

DB_URL = 'postgresql://admin:password123@db:5432/analytics'

def load_data(file_path):
    print(f"Спроба завантажити дані з: {file_path}")
    try:
        df = pd.read_csv(file_path, sep=';', low_memory=False)
        print("Дані успішно зчитано з CSV.")
        print(f"Розмір датасету: {df.shape[0]} рядків та {df.shape[1]} колонок.")
        return df
    except FileNotFoundError:
        print(f"Помилка: Файл {file_path} не знайдено.")
        return None
    except Exception as e:
        print(f"Неочікувана помилка під час завантаження: {e}")
        return None

def save_to_db(df):
    print("Підключення до бази даних PostgreSQL...")
    engine = create_engine(DB_URL)
    
    for i in range(5):
        try:
            df.to_sql('appeals', engine, if_exists='replace', index=False)
            print("УСПІХ: Дані збережено у базу даних PostgreSQL (таблиця 'appeals')!")
            return
        except OperationalError:
            print("База даних ще не готова. Чекаємо 5 секунд...")
            time.sleep(5)
            
    print("ПОМИЛКА: Не вдалося підключитися до бази даних.")

if __name__ == "__main__":
    dataset = load_data(RAW_DATA_PATH)
    
    if dataset is not None:
        save_to_db(dataset)