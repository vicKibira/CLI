import click
import os
import pandas as pd
from data_eng_cli.transform import transform_data
from data_eng_cli.load import load
from data_eng_cli.extract import (
    extract_from_file,
    extract_from_directory,
    extract_from_api,
)

TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp_data")

@click.group()
def cli():
    """Data Eng CLI - A simple ETL tool"""
    pass

@click.command()
@click.argument("file_path")
def extract_file(file_path):
    """Extract data from a file (CSV, JSON, Parquet)"""
    try:
        temp_file = extract_from_file(file_path)
        click.echo(f"Extracted data saved to {temp_file}")
    except Exception as e:
        click.echo(f"Error: {e}")

@click.command()
@click.argument("directory")
def extract_directory(directory):
    """Extract data from a directory"""
    try:
        extracted_files = extract_from_directory(directory)
        click.echo(f"Extracted {len(extracted_files)} files. Check temp_data/")
    except Exception as e:
        click.echo(f"Error: {e}")

@click.command()
@click.argument("url")
@click.option("--format", type=click.Choice(["csv", "json", "parquet"], case_sensitive=False), default="json")
def extract_api(url, format):
    """Extract data from an API"""
    try:
        temp_file = extract_from_api(url, format)
        click.echo(f"Extracted data saved to {temp_file}")
    except Exception as e:
        click.echo(f"Error: {e}")

@click.command()
@click.argument("filename")
@click.option("--dropna", is_flag=True, help="Drop missing values")
@click.option("--rename", multiple=True, help="Rename columns using 'old:new' format")
@click.option("--filter-col", help="Column name to filter on")
@click.option("--filter-val", help="Value to filter by")
def transform(filename, dropna, rename, filter_col, filter_val):
    """Transform data"""
    try:
        transform_data(filename, dropna, rename, filter_col, filter_val)
    except Exception as e:
        click.echo(f"Error: {e}")

@click.command()
@click.argument("filename")
@click.argument("db_type")
@click.option("--table", default="etl_data", help="Target table name")
def load_data(filename, db_type, table):
    """Load data into a database"""
    load.main([filename, db_type, "--table", table])

cli.add_command(transform)
cli.add_command(extract_file)
cli.add_command(extract_directory)
cli.add_command(extract_api)
cli.add_command(load_data)

if __name__ == "__main__":
    cli()
# import click
# import os
# import pandas as pd
# from data_eng_cli.transform import transform_data
# from data_eng_cli.load import load
# from data_eng_cli.extract import (
#     extract_from_file,
#     extract_from_directory,
#     extract_from_api,
# )

# TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp_data")


# @click.group()
# def cli():
#     """Data Eng CLI - A simple ETL tool"""
#     pass


# @click.command()
# @click.argument("file_path")
# def extract_file(file_path):
#     """Extract data from a file (CSV, JSON, Parquet)"""
#     try:
#         temp_file = extract_from_file(file_path)
#         click.echo(f"Extracted data saved to {temp_file}")
#     except Exception as e:
#         click.echo(f"Error: {e}")


# @click.command()
# @click.argument("directory")
# def extract_directory(directory):
#     """Extract data from a directory"""
#     try:
#         extracted_files = extract_from_directory(directory)
#         click.echo(f"Extracted {len(extracted_files)} files. Check temp_data/")
#     except Exception as e:
#         click.echo(f"Error: {e}")


# @click.command()
# @click.argument("url")
# @click.option("--format", type=click.Choice(["csv", "json", "parquet"], case_sensitive=False), default="json")
# def extract_api(url, format):
#     """Extract data from an API"""
#     try:
#         temp_file = extract_from_api(url, format)
#         click.echo(f"Extracted data saved to {temp_file}")
#     except Exception as e:
#         click.echo(f"Error: {e}")


# @click.command()
# @click.argument("filename")
# @click.option("--dropna", is_flag=True, help="Drop missing values")
# @click.option("--rename", multiple=True, help="Rename columns using 'old:new' format")
# @click.option("--filter-col", help="Column name to filter on")
# @click.option("--filter-val", help="Value to filter by")
# def transform(filename, dropna, rename, filter_col, filter_val):
#     """Transform data"""
#     try:
#         transform_data(filename, dropna, rename, filter_col, filter_val)
#     except Exception as e:
#         click.echo(f"Error: {e}")


# @click.command()
# @click.argument("filename")
# @click.argument("db_type")
# @click.option("--table", default="etl_data", help="Target table name")
# def load_data(filename, db_type, table):
#     """Load data into a database"""
#     try:
#         # Ensure load.py has a function that accepts these parameters
#         load(filename, db_type, table)
#         click.echo(f"Data from {filename} loaded into {db_type}, table: {table}")
#     except Exception as e:
#         click.echo(f"Error: {e}")


# # Register commands with CLI
# cli.add_command(transform)
# cli.add_command(extract_file)
# cli.add_command(extract_directory)
# cli.add_command(extract_api)
# cli.add_command(load_data)


# if __name__ == "__main__":
#     cli(prog_name="data-eng-cli")
