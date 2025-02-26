# Data Eng CLI

A simple command-line tool for common data engineering tasks such as extracting, transforming, and loading data.

## Features

- **Extract Data**
  - **File Extraction:** Extract data from CSV, JSON, or Parquet files using the `extract-file` command.
  - **Directory Extraction:** Extract data from all supported file formats within a directory using the `extract-directory` command.
  - **API Extraction:** Retrieve data from an API endpoint in CSV, JSON, or Parquet format using the `extract-api` command.
- **Transform Data**
  - Clean, rename, and filter your data with the `transform` command.
- **Load Data**
  - Load your transformed data into various databases (e.g., PostgreSQL, MySQL, SQLite, DuckDB, BigQuery, and Snowflake) using the `load-data` command.

## Installation

You can install the CLI tool directly from GitHub using pip. This method does not require you to clone the repository manually—the package is built and installed automatically.

Open your terminal and run:

```bash
pip install git+https://github.com/vicKibira/CLI.git
If you ever update the tool on GitHub, you (or your users) can update to the latest version with:

bash
Copy
Edit
pip install --upgrade git+https://github.com/vicKibira/CLI.git
Usage
Once installed, the CLI tool will be available globally as data-eng-cli.

Display Help
To see the available commands and usage options, run:

bash
Copy
Edit
data-eng-cli --help
You should see output similar to:

kotlin
Copy
Edit
Usage: data-eng-cli [OPTIONS] COMMAND [ARGS]...

Data Eng CLI - A simple ETL tool

Options:
  --help  Show this message and exit.

Commands:
  extract-api
  extract-directory
  extract-file
  load-data
  transform
Examples
1. Extract Data from a File
To extract data from a CSV file:

bash
Copy
Edit
data-eng-cli extract-file path/to/your/file.csv
2. Extract Data from a Directory
To extract all supported files from a directory:

bash
Copy
Edit
data-eng-cli extract-directory path/to/your/directory
3. Extract Data from an API
To extract data from an API endpoint (for example, in JSON format):

bash
Copy
Edit
data-eng-cli extract-api "https://api.example.com/data" --format json
4. Transform Data
To transform your data by cleaning, renaming, or filtering:

bash
Copy
Edit
data-eng-cli transform path/to/your/file.csv --dropna --rename old_column:new_column --filter-col age --filter-val 30
5. Load Data into a Database
To load transformed data into a database (for example, into MySQL):

bash
Copy
Edit
data-eng-cli load-data path/to/your/file.csv mysql --table your_table
When running the load command, you’ll be prompted to enter any missing database credentials interactively (or you can provide them via CLI options).

Requirements
Python 3.7 or later
Dependencies (installed automatically via pip):
click
pandas
requests
pyyaml
sqlalchemy
duckdb
pymysql
google-cloud-bigquery
snowflake-connector-python
Contributing
Contributions, issues, and feature requests are welcome!
Feel free to open an issue or submit a pull request on GitHub.

License
This project is licensed under the MIT License.

pgsql
Copy
Edit

---

### How to Download

1. **Copy the entire text** above (from `# Data Eng CLI` to the end).
2. **Paste it into a new file** in your text editor.
3. **Save the file as `README.md`** in your project’s root directory.

This file is now ready to be included in your repository or distributed as needed. Enjoy!





