import pandas as pd
import os

# This will define the file paths
RAW_DATA_PATH = "data/alzheimers_trials_raw.csv"
CLEAN_DATA_PATH = "data/alzheimers_trials_clean.csv"

def load_data(path):
    """loading the the raw clinical trials dataset."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    print(f"✅ Loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def clean_columns(df):
    """Standardize column names: lowercase and no spaces."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def clean_text_fields(df, fields):
    """Strip whitespace and lowercase string fields."""
    for col in fields:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    return df

def convert_dates(df, fields):
    """Convert date columns to datetime."""
    for col in fields:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def handle_missing(df):
    """Drop rows with critical missing values."""
    if "study_title" in df.columns:
        df = df.dropna(subset=["study_title"])
    return df

def save_data(df, path):
    """Save cleaned dataframe to CSV."""
    df.to_csv(path, index=False)
    print(f"✅ Cleaned data saved to {path}")

def main():
    print("🧹 Starting data cleaning...")
    
    df = load_data(RAW_DATA_PATH)
    
    df = clean_columns(df)
    
    df = clean_text_fields(df, fields=["study_status", "conditions", "interventions", "sponsor", "study_type", "sex", "age", "locations"])
    
    df = convert_dates(df, fields=["start_date", "completion_date"])
    
    df = handle_missing(df)
    
    save_data(df, CLEAN_DATA_PATH)
    print("Data cleaning complete")

if __name__ == "__main__":
    main()
