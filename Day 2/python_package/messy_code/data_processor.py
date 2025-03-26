import pandas as pd
import numpy as np
from typing import List, Dict, Union

def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic data cleaning operations."""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.fillna(df.mean(numeric_only=True))
    
    return df

def filter_by_column(df: pd.DataFrame, column: str, condition: callable) -> pd.DataFrame:
    """Filter DataFrame based on a condition for a specific column."""
    return df[condition(df[column])]

def save_csv(df: pd.DataFrame, file_path: str) -> None:
    """Save DataFrame to CSV."""
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    # Example usage
    df = load_csv("example.csv")
    df = clean_data(df)
    filtered_df = filter_by_column(df, "age", lambda x: x > 30)
    save_csv(filtered_df, "output.csv") 