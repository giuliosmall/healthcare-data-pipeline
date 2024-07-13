#!/usr/bin/env python3
import pandas as pd
import logging
from datetime import datetime
import argparse

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()

    # ensure 'start' and 'stop' are datetime
    df['start'] = pd.to_datetime(df['start'], errors='coerce')
    df['stop'] = pd.to_datetime(df['stop'], errors='coerce')

    # drop rows where 'start' or 'stop' could not be converted to datetime
    df = df.dropna(subset=['start', 'stop'])

    # create a surrogate key to remove duplicates
    df['surrogate_key'] = df['patient'].astype(str) + '-' + df['encounter'].astype(str) + '-' + df['code'].astype(str)
    df = df.drop_duplicates(subset=['surrogate_key'])

    # duration of the procedure in seconds
    df.loc[:, 'duration_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

    # breakdown timestamp details
    df.loc[:, 'year'] = df['start'].dt.year
    df.loc[:, 'month'] = df['start'].dt.strftime('%B')
    df.loc[:, 'week'] = df['start'].dt.isocalendar().week
    df.loc[:, 'day'] = df['start'].dt.strftime('%A')

    return df

def save_cleaned_data(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)

def process_data(file_path: str, output_path: str, base_cost_limit: float):
    start_time = datetime.now()
    logging.info(f"Started cleaning procedures data at {start_time}")

    df = read_data(file_path)
    total_rows = len(df)
    logging.info(f"Total rows in the dataset: {total_rows}")

    cleaned_df = clean_data(df)
    rows_after_cleaning = len(cleaned_df)
    logging.info(f"Rows after cleaning: {rows_after_cleaning}")

    # exclude procedures more expensive than base_cost_limit
    cleaned_df = cleaned_df[cleaned_df['base_cost'] <= base_cost_limit]
    rows_after_cost_filter = len(cleaned_df)
    logging.info(f"Total rows after filtering by cost: {rows_after_cost_filter}")

    # drop the surrogate key column
    cleaned_df = cleaned_df.drop(columns=['surrogate_key'])

    save_cleaned_data(cleaned_df, output_path)

    end_time = datetime.now()
    logging.info(f"Finished cleaning procedures data at {end_time}")
    logging.info(f"Total processing time: {end_time - start_time}")
    logging.info(f"Total rows processed: {total_rows}")
    logging.info(f"Total rows before cost filter: {rows_after_cleaning}")
    logging.info(f"Total rows after cost filter: {rows_after_cost_filter}")
    percentage_removed = 100 * (total_rows - rows_after_cost_filter) / total_rows
    logging.info(f"Percentage of rows removed from the original dataset: {percentage_removed:.2f}%")
    logging.info(f"Output file saved as: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Clean procedures.csv.')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('output_file', help='Path to the output cleaned CSV file')
    # optional argument for base_cost_limit
    parser.add_argument('--base_cost_limit', type=float, default=30000, help='Base cost limit for filtering procedures')
    args = parser.parse_args()

    process_data(args.input_file, args.output_file, base_cost_limit=args.base_cost_limit)

if __name__ == '__main__':
    main()