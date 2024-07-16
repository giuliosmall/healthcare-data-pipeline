import pandas as pd
from sqlalchemy import create_engine
import yaml
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def upload_to_postgres(file_path, table_name, db_url):
    engine = create_engine(db_url)
    df = pd.read_csv(file_path)

    logging.info(f"Uploading {file_path} to {table_name} table.")
    logging.info(f"Data shape: {df.shape}")

    # lowercase all column names
    df.columns = df.columns.str.lower()

    df.to_sql(table_name, engine, if_exists='replace', index=False)
    logging.info(f"Uploaded {file_path} to {table_name} table.")


if __name__ == "__main__":
    with open("/app/config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    db_url = config['database']['url']

    files_to_upload = {
        "data/encounters_cleaned.csv": "encounters",
        "data/organizations.csv": "organizations",
        "data/patients.csv": "patients",
        "data/payers.csv": "payers",
        "data/procedures.csv": "procedures"
    }

    for file_path, table_name in files_to_upload.items():
        upload_to_postgres(file_path, table_name, db_url)