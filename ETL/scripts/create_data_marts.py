from sqlalchemy import create_engine, text
import yaml
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_queries(filename):
    """
    Load SQL queries from a file. The queries are separated by a semicolon.
    """
    with open(filename, 'r') as file:
        queries = file.read().split(';')
        queries = [query.strip() for query in queries if query.strip()]
    return queries


def create_data_marts(engine, queries):
    """
    Create data marts and analysis tables in the database.
    """
    with engine.begin() as conn:  # use engine.begin() to handle multiple transactions
        try:
            logging.info("Dropping existing data marts if they exist.")
            conn.execute(text("DROP TABLE IF EXISTS united_healthcare_data;"))
            conn.execute(text("DROP TABLE IF EXISTS humana_data;"))
            conn.execute(text("DROP TABLE IF EXISTS payer_ranking;"))
            conn.execute(text("DROP TABLE IF EXISTS top_5_patients;"))
            conn.execute(text("DROP TABLE IF EXISTS top_5_procedures_daily;"))

            for query in queries:
                logging.info(f"Executing query: {query[:30]}...") # log only the start of the query
                conn.execute(text(query))

            logging.info("Data marts and analysis tables created successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    with open("/app/config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    db_url = config['database']['url']
    engine = create_engine(db_url)

    queries = load_queries("/app/scripts/queries.sql")
    create_data_marts(engine, queries)