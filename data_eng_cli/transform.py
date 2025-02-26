import os
import pandas as pd
import click

TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp_data")

def transform_data(filename, dropna=False, rename=None, filter_col=None, filter_val=None):
    """Perform basic transformations on extracted data."""
    
    file_path = os.path.join(TEMP_DIR, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f" File not found: {filename}")

    file_ext = filename.split(".")[-1].lower()

    try:
        if file_ext == "csv":
            df = pd.read_csv(file_path)
        elif file_ext == "json":
            df = pd.read_json(file_path)
        elif file_ext == "parquet":
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(" Unsupported file format.")

        click.echo(f"Transforming {filename}...")

        # Drop missing values if specified
        if dropna:
            df.dropna(inplace=True)
            click.echo("Dropped missing values.")

        # Rename columns if specified
        if rename:
            rename_dict = dict(pair.split(":") for pair in rename)
            df.rename(columns=rename_dict, inplace=True)
            click.echo(f" Renamed columns: {rename_dict}")

        # Filter rows if specified
        if filter_col and filter_val:
            df = df[df[filter_col] == filter_val]
            click.echo(f" Filtered rows where {filter_col} == {filter_val}")

        # Save the transformed file
        transformed_filename = f"transformed_{filename}"
        transformed_path = os.path.join(TEMP_DIR, transformed_filename)

        if file_ext == "csv":
            df.to_csv(transformed_path, index=False)
        elif file_ext == "json":
            df.to_json(transformed_path, orient="records", lines=True)
        elif file_ext == "parquet":
            df.to_parquet(transformed_path, index=False)

        click.echo(f"Transformed data saved as {transformed_filename}")

    except Exception as e:
        click.echo(f"Error: {e}")
