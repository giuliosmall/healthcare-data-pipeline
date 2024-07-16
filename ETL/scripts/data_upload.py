import pandas as pd
from sqlalchemy import create_engine
import yaml
import logging
import os
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import pandas as pd
from sqlalchemy import create_engine
import yaml
import logging
import os
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_to_postgres(file_path, table_name, engine):
    """
    Upload a CSV file to a PostgreSQL table.
    """
    try:
        df = pd.read_csv(file_path)

        logging.info(f"Uploading {file_path} to {table_name} table.")
        logging.info(f"Data shape: {df.shape}")

        # lowercase all column names
        df.columns = df.columns.str.lower()

        # check for empty dataframe
        if df.empty:
            logging.warning(f"{file_path} is empty. Skipping upload.")
            return

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Uploaded {file_path} to {table_name} table successfully.")
    except Exception as e:
        logging.error(f"Failed to upload {file_path} to {table_name} table: {e}")

if __name__ == "__main__":
    try:
        with open("/app/config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)

        db_url = config['database']['url']
        files_to_upload = config.get('files', {})

        for file_path, table_name in files_to_upload.items():
            if os.path.exists(file_path):
                upload_to_postgres(file_path, table_name, db_url)
            else:
                logging.warning(f"File {file_path} does not exist. Skipping.")
    except Exception as e:
        logging.error(f"ETL process failed: {e}")