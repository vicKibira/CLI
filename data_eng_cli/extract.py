import os
import pandas as pd
import requests
from io import StringIO, BytesIO

# Create a temp directory if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp_data")
os.makedirs(TEMP_DIR, exist_ok=True)

def save_to_temp(df, filename):
    """Save extracted DataFrame to a temp CSV file."""
    file_path = os.path.join(TEMP_DIR, filename)
    df.to_csv(file_path, index=False)
    return file_path

def extract_from_file(file_path: str):
    """Extract data from a CSV, JSON, or Parquet file and save to temp."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_ext = file_path.split(".")[-1].lower()
    
    if file_ext == "csv":
        df = pd.read_csv(file_path)
    elif file_ext == "json":
        df = pd.read_json(file_path)
    elif file_ext == "parquet":
        df = pd.read_parquet(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV, JSON, or Parquet.")

    return save_to_temp(df, os.path.basename(file_path))

def extract_from_directory(directory: str):
    """Extract all CSV, JSON, and Parquet files from a given directory and save to temp."""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    extracted_files = []

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            try:
                temp_file = extract_from_file(file_path)
                extracted_files.append(temp_file)
            except ValueError as e:
                print(f"Skipping {file}: {e}")

    return extracted_files

def extract_from_api(url: str, format: str = "json"):
    """
    Extract data from an API in CSV, JSON, or Parquet format and save to temp.
    """
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f" Failed to fetch data. Status Code: {response.status_code}")

    format = format.lower()
    
    if format == "json":
        df = pd.DataFrame(response.json())

    elif format == "csv":
        df = pd.read_csv(StringIO(response.text))

    elif format == "parquet":
        df = pd.read_parquet(BytesIO(response.content))

    else:
        raise ValueError("Unsupported format. Choose from: csv, json, parquet.")

    filename = f"api_data.{format}"
    return save_to_temp(df, filename)
