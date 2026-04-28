import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

DB_URL = 'postgresql://admin:password123@db:5432/analytics'
SHARED_DIR = '/shared_data'

def create_visualizations():
    print("Підключення до бази даних...")
    engine = create_engine(DB_URL)
    
    df = None
    for i in range(5):
        try:
            df = pd.read_sql('appeals_modeled', engine)
            break
        except Exception:
            print("Очікування таблиці 'appeals_modeled'...")
            time.sleep(5)
            
    if df is None:
        print("Помилка: не вдалося завантажити дані з БД.")
        return

    os.makedirs(SHARED_DIR, exist_ok=True)
    print("=== Visualization ===")

    df['registrationDate'] = pd.to_datetime(df['registrationDate'], errors='coerce')
    df['executionDate'] = pd.to_datetime(df['executionDate'], errors='coerce')

    plt.figure(figsize=(10, 10))
    sns.scatterplot(
        data=df, x='longitude', y='latitude', 
        hue='district', palette='viridis', alpha=0.5, s=10
    )
    plt.title("Географічний розподіл звернень за районами Львова (2024)", fontsize=15)
    plt.xlabel("Довгота")
    plt.ylabel("Широта")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(SHARED_DIR, "geo_distribution.png"))
    plt.close()

    plt.figure(figsize=(12, 6))
    top_10 = df['category'].value_counts().head(10).reset_index()
    top_10.columns = ['Category', 'Count']
    sns.barplot(data=top_10, x='Count', y='Category', palette='magma')
    plt.title("Топ-10 категорій звернень на Гарячу лінію", fontsize=15)
    plt.xlabel("Кількість звернень")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(SHARED_DIR, "top_categories.png"))
    plt.close()

    df['execution_time_days'] = (df['executionDate'] - df['registrationDate']).dt.days
    df_filtered = df[(df['execution_time_days'] >= 0) & (df['execution_time_days'] <= 60)]

    plt.figure(figsize=(14, 7))
    sns.boxplot(data=df_filtered, x='district', y='execution_time_days', palette='Set3')
    plt.title("Розподіл часу виконання звернень за районами (до 60 днів)", fontsize=15)
    plt.xlabel("Район")
    plt.ylabel("Дні виконання")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(SHARED_DIR, "district_efficiency.png"))
    plt.close()

    plt.figure(figsize=(12, 5))
    df['month'] = df['registrationDate'].dt.to_period('M').astype(str)
    monthly_trends = df.groupby('month').size().reset_index(name='count')
    sns.lineplot(data=monthly_trends, x='month', y='count', marker='o', color='red', linewidth=2.5)
    plt.title("Динаміка надходження звернень протягом 2024 року", fontsize=15)
    plt.xlabel("Місяць")
    plt.ylabel("Кількість")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(SHARED_DIR, "monthly_trends.png"))
    plt.close()


if __name__ == "__main__":
    create_visualizations()