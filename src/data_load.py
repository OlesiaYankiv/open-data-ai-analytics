import pandas as pd
import os

RAW_DATA_PATH = os.path.join("data", "raw", "glm_all_2024_portal.csv")

def load_data(file_path):
    print(f"Attempting to load data from: {file_path}")
    try:
        df = pd.read_csv(file_path, sep=';', low_memory=False)
        print(f"Successfully loaded data")
        print(f"Dataset shape: {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during data loading: {e}")
        return None

if __name__ == "__main__":
    dataset = load_data(RAW_DATA_PATH)
    
    if dataset is not None:
        print("\nFirst 5 rows of the dataset:")
        print(dataset.head())