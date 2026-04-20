import pandas as pd

def run_quality_checks(df):
    print("=== Data Analysis ===")
    
    cols_of_interest = [
        'latitude', 'longitude', 'category', 'type', 'appealSource', 
        'registrationDate', 'executionDate', 'executionStatus', 'executantName', 'district'
    ]
    
    print(f"\nData size: {df.shape[0]} rows, {df.shape[1]} columns")
    
    for col in ['latitude', 'longitude']:
        df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = df[col].str.rstrip('.')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    print("\n--- Missing Values in Key Columns ---")
    missing_data = df[cols_of_interest].isnull().sum()
    print(missing_data[missing_data > 0])
    
    df['registrationDate'] = pd.to_datetime(df['registrationDate'], errors='coerce')
    df['executionDate'] = pd.to_datetime(df['executionDate'], errors='coerce')
    
    df_cleaned = df.dropna(subset=['latitude', 'longitude', 'registrationDate'])
    
    duplicates = df_cleaned.duplicated().sum()
    print(f"\nNumber of duplicate rows after cleaning: {duplicates}")
    df_cleaned = df_cleaned.drop_duplicates()
    
    print(f"\nData size after cleaning: {df_cleaned.shape[0]} rows", f"{df_cleaned.shape[1]} columns")
    return df_cleaned

if __name__ == "__main__":
    import os
    from data_load import load_data
    
    RAW_DATA_PATH = os.path.join("data", "raw", "glm_all_2024_portal.csv")
    df = load_data(RAW_DATA_PATH)
    
    if df is not None:
        cleaned_df = run_quality_checks(df)