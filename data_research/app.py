import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import time
import os

DB_URL = 'postgresql://admin:password123@db:5432/analytics'
SHARED_DIR = '/shared_data'

def analyze_and_model():
    print("Підключення до бази даних...")
    engine = create_engine(DB_URL)
    
    df = None
    for i in range(5):
        try:
            df = pd.read_sql('appeals_cleaned', engine)
            break
        except Exception:
            print("Очікування таблиці 'appeals_cleaned'...")
            time.sleep(5)
            
    if df is None:
        print("Помилка: не вдалося завантажити очищені дані з БД.")
        return

    report = []
    report.append("=== Data Research ===")
    
    report.append("\n--- 1. Географічний розподіл та проблемні райони ---")
    coords = df[['latitude', 'longitude']].dropna()
    kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
    df.loc[coords.index, 'geo_cluster'] = kmeans.fit_predict(coords)
    
    report.append("Концентрація звернень по адміністративних районах:")
    report.append(df['district'].value_counts().to_string())
    
    report.append("\n--- 2. Топ-10 тематичних категорій ---")
    top_10 = df['category'].value_counts().head(10)
    total_appeals = len(df)
    
    for cat, count in top_10.items():
        percentage = (count / total_appeals) * 100
        report.append(f"- {cat}: {count} ({percentage:.2f}%)")
        
    report.append("\nРозбивка Топ-3 категорій за типом та джерелом:")
    top_3_cats = top_10.head(3).index
    breakdown = df[df['category'].isin(top_3_cats)].groupby(
        ['category', 'type', 'appealSource']
    ).size().reset_index(name='count')
    report.append(breakdown.to_string())

    report.append("\n--- 3. Ефективність обробки заявок ---")

    df['registrationDate'] = pd.to_datetime(df['registrationDate'])
    df['executionDate'] = pd.to_datetime(df['executionDate'])
    df['execution_time_days'] = (df['executionDate'] - df['registrationDate']).dt.days
    
    executed_df = df[(df['executionStatus'] == 'Виконано') & (df['execution_time_days'] >= 0)]
    
    avg_time = executed_df['execution_time_days'].mean()
    report.append(f"Середній час виконання всіх звернень: {avg_time:.2f} днів")
    
    report.append("\nЕфективність топ-5 виконавців (за кількістю заявок):")
    top_executants = executed_df['executantName'].value_counts().head(5).index
    executant_efficiency = executed_df[executed_df['executantName'].isin(top_executants)].groupby(
        'executantName'
    )['execution_time_days'].agg(['mean', 'count']).sort_values(by='mean')
    
    report.append(executant_efficiency.rename(columns={'mean': 'Середній час (дні)', 'count': 'К-ть заявок'}).to_string())

    os.makedirs(SHARED_DIR, exist_ok=True)
    with open(os.path.join(SHARED_DIR, 'research_report.txt'), 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    df.to_sql('appeals_modeled', engine, if_exists='replace', index=False)
    
    print("\n".join(report))
    print("\nДослідження завершено. Результати збережено.")

if __name__ == "__main__":
    analyze_and_model()