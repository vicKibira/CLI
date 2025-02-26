import click
import pandas as pd
import sqlalchemy
from google.cloud import bigquery
import snowflake.connector  

# Function to get credentials (interactively if not provided)
def get_db_credentials(db_type, host, port, database, user, password, schema):
    credentials = {}

    if db_type in ["postgres", "mysql"]:
        credentials["host"] = host or click.prompt("Enter database host", default="localhost")
        credentials["port"] = port or click.prompt("Enter port", type=int)
        credentials["database"] = database or click.prompt("Enter database name")
        credentials["user"] = user or click.prompt("Enter username")
        credentials["password"] = password or click.prompt("Enter password", hide_input=True)

    elif db_type == "sqlite":
        credentials["database"] = database or click.prompt("Enter SQLite file path", default="data_eng.sqlite")

    elif db_type == "duckdb":
        credentials["database"] = database or click.prompt("Enter DuckDB file path", default="data_eng.duckdb")

    elif db_type == "bigquery":
        credentials["project_id"] = click.prompt("Enter GCP Project ID")
        credentials["dataset_id"] = click.prompt("Enter BigQuery Dataset ID")

    elif db_type == "snowflake":
        credentials["account"] = click.prompt("Enter Snowflake account (e.g., xyz123.snowflakecomputing.com)")
        credentials["user"] = user or click.prompt("Enter Snowflake username")
        credentials["password"] = password or click.prompt("Enter Snowflake password", hide_input=True)
        credentials["database"] = database or click.prompt("Enter Snowflake database")
        credentials["schema"] = schema or click.prompt("Enter Snowflake schema")

    return credentials

# Establish database connection
def get_db_connection(db_type, credentials):
    if db_type == "postgres":
        conn_str = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}"
        return sqlalchemy.create_engine(conn_str)

    elif db_type == "mysql":
        conn_str = f"mysql+pymysql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}"
        return sqlalchemy.create_engine(conn_str)

    elif db_type == "sqlite":
        return sqlalchemy.create_engine(f"sqlite:///{credentials['database']}")

    elif db_type == "duckdb":
        return sqlalchemy.create_engine(f"duckdb:///{credentials['database']}")

    elif db_type == "bigquery":
        return bigquery.Client(project=credentials["project_id"])

    elif db_type == "snowflake":
        return snowflake.connector.connect(
            account=credentials["account"],
            user=credentials["user"],
            password=credentials["password"],
            database=credentials["database"],
            schema=credentials["schema"]
        )

# Load data into database
@click.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("db_type")
@click.option("--table", default="etl_data", help="Target table name")
@click.option("--host", default=None, help="Database host")
@click.option("--port", default=None, type=int, help="Database port")
@click.option("--database", default=None, help="Database name")
@click.option("--user", default=None, help="Database username")
@click.option("--password", default=None, help="Database password")
@click.option("--schema", default=None, help="Schema name (for Snowflake)")
def load(file_path, db_type, table, host, port, database, user, password, schema):
    """Load transformed data into a database"""

    credentials = get_db_credentials(db_type, host, port, database, user, password, schema)
    engine = get_db_connection(db_type, credentials)

    # Read file into a DataFrame
    if file_path.endswith(".csv"):
        data = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        data = pd.read_json(file_path)
    elif file_path.endswith(".parquet"):
        data = pd.read_parquet(file_path)
    else:
        click.echo("❌ Unsupported file format.")
        return

    click.echo(f"✅ Successfully loaded data from {file_path}")

    # Load into database
    if db_type in ["postgres", "mysql", "sqlite", "duckdb"]:
        data.to_sql(table, engine, if_exists="replace", index=False)
        click.echo(f"✅ Data loaded into {db_type} -> {table}")

    elif db_type == "bigquery":
        table_id = f"{credentials['project_id']}.{credentials['dataset_id']}.{table}"
        job = engine.load_table_from_dataframe(data, table_id)
        job.result()  # Wait for the job to complete
        click.echo(f"✅ Data loaded into BigQuery -> {table_id}")

    elif db_type == "snowflake":
        cursor = engine.cursor()
        columns = ", ".join(data.columns)
        values_placeholder = ", ".join(["%s"] * len(data.columns))
        query = f"INSERT INTO {credentials['schema']}.{table} ({columns}) VALUES ({values_placeholder})"
        cursor.executemany(query, data.values.tolist())
        engine.commit()
        click.echo(f"✅ Data loaded into Snowflake -> {credentials['schema']}.{table}")

if __name__ == "__main__":
     load()