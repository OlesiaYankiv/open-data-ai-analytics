import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def create_visualizations(df):

    output_dir = os.path.join("reports", "figures")
    os.makedirs(output_dir, exist_ok=True)

    print("=== Visualization ===")

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
    plt.savefig(os.path.join(output_dir, "geo_distribution.png"))


    plt.figure(figsize=(12, 6))
    top_10 = df['category'].value_counts().head(10).reset_index()
    top_10.columns = ['Category', 'Count']
    
    sns.barplot(data=top_10, x='Count', y='Category', palette='magma')
    plt.title("Топ-10 категорій звернень на Гарячу лінію", fontsize=15)
    plt.xlabel("Кількість звернень")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "top_categories.png"))


    df['execution_time_days'] = (df['executionDate'] - df['registrationDate']).dt.days
    df_filtered = df[(df['execution_time_days'] >= 0) & (df['execution_time_days'] <= 60)]

    plt.figure(figsize=(14, 7))
    sns.boxplot(data=df_filtered, x='district', y='execution_time_days', palette='Set3')
    plt.title("Розподіл часу виконання звернень за районами (до 60 днів)", fontsize=15)
    plt.xlabel("Район")
    plt.ylabel("Дні виконання")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "district_efficiency.png"))

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
    plt.savefig(os.path.join(output_dir, "monthly_trends.png"))

if __name__ == "__main__":
    from data_load import load_data
    from data_quality_analysis import run_quality_checks
    
    RAW_DATA_PATH = os.path.join("data", "raw", "glm_all_2024_portal.csv")
    df = load_data(RAW_DATA_PATH)
    
    if df is not None:
        cleaned_df = run_quality_checks(df)
        create_visualizations(cleaned_df)