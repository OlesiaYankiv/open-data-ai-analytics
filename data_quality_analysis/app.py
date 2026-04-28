import pandas as pd
from sqlalchemy import create_engine
import time
import os

DB_URL = 'postgresql://admin:password123@db:5432/analytics'
SHARED_DIR = '/shared_data'

def run_quality_checks():
    print("Підключення до бази даних...")
    engine = create_engine(DB_URL)
    
    df = None
    for i in range(5):
        try:
            df = pd.read_sql('appeals', engine)
            break
        except Exception:
            print("Очікування таблиці 'appeals'...")
            time.sleep(5)
            
    if df is None:
        print("Помилка: не вдалося завантажити дані з БД.")
        return

    report = []
    report.append("=== Data Quality Analysis ===")
    
    cols_of_interest = [
        'latitude', 'longitude', 'category', 'type', 'appealSource', 
        'registrationDate', 'executionDate', 'executionStatus', 'executantName', 'district'
    ]
    
    report.append(f"\nПочатковий розмір: {df.shape[0]} рядків, {df.shape[1]} колонок")
    
    for col in ['latitude', 'longitude']:
        df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = df[col].str.rstrip('.')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    report.append("\n--- Пропущені значення у ключових колонках ---")
    missing_data = df[cols_of_interest].isnull().sum()
    missing_str = missing_data[missing_data > 0].to_string()
    report.append(missing_str if missing_str else "Пропусків немає.")
    
    df['registrationDate'] = pd.to_datetime(df['registrationDate'], errors='coerce')
    df['executionDate'] = pd.to_datetime(df['executionDate'], errors='coerce')
    
    df_cleaned = df.dropna(subset=['latitude', 'longitude', 'registrationDate'])
    
    duplicates = df_cleaned.duplicated().sum()
    report.append(f"\nКількість дублікатів: {duplicates}")
    df_cleaned = df_cleaned.drop_duplicates()
    
    report.append(f"\nРозмір після очищення: {df_cleaned.shape[0]} рядків, {df_cleaned.shape[1]} колонок")
    
    os.makedirs(SHARED_DIR, exist_ok=True)
    with open(os.path.join(SHARED_DIR, 'quality_report.txt'), 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    df_cleaned.to_sql('appeals_cleaned', engine, if_exists='replace', index=False)
    
    print("\n".join(report))
    print("\nОчищення завершено. Дані збережено в 'appeals_cleaned'.")

if __name__ == "__main__":
    run_quality_checks()