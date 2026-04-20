import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def analyze_and_model(df):
    print("\n=== Data Research ===")
    
    print("\n--- 1. Географічний розподіл та проблемні райони ---")
    coords = df[['latitude', 'longitude']].dropna()
    kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
    df.loc[coords.index, 'geo_cluster'] = kmeans.fit_predict(coords)
    
    print("Концентрація звернень по адміністративних районах:")
    district_counts = df['district'].value_counts()
    print(district_counts)
    
    print("\n--- 2. Топ-10 тематичних категорій ---")
    top_10 = df['category'].value_counts().head(10)
    total_appeals = len(df)
    
    for cat, count in top_10.items():
        percentage = (count / total_appeals) * 100
        print(f"- {cat}: {count} ({percentage:.2f}%)")
        
    print("\nРозбивка Топ-3 категорій за типом та джерелом:")
    top_3_cats = top_10.head(3).index
    breakdown = df[df['category'].isin(top_3_cats)].groupby(
        ['category', 'type', 'appealSource']
    ).size().reset_index(name='count')
    print(breakdown)

    print("\n--- 3. Ефективність обробки заявок ---")
    df['execution_time_days'] = (df['executionDate'] - df['registrationDate']).dt.days
    
    executed_df = df[(df['executionStatus'] == 'Виконано') & (df['execution_time_days'] >= 0)]
    
    avg_time = executed_df['execution_time_days'].mean()
    print(f"Середній час виконання всіх звернень: {avg_time:.2f} днів")
    
    print("\nЕфективність топ-5 виконавців (за кількістю заявок):")
    top_executants = executed_df['executantName'].value_counts().head(5).index
    executant_efficiency = executed_df[executed_df['executantName'].isin(top_executants)].groupby(
        'executantName'
    )['execution_time_days'].agg(['mean', 'count']).sort_values(by='mean')
    
    print(executant_efficiency.rename(columns={'mean': 'Середній час (дні)', 'count': 'К-ть заявок'}))


if __name__ == "__main__":
    import os
    from data_load import load_data
    from data_quality_analysis import run_quality_checks
    
    RAW_DATA_PATH = os.path.join("data", "raw", "glm_all_2024_portal.csv")
    df = load_data(RAW_DATA_PATH)
    
    if df is not None:
        cleaned_df = run_quality_checks(df)
        analyze_and_model(cleaned_df)