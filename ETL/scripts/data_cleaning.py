import pandas as pd

def read_data(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data by converting columns to lowercase, converting 'start' and 'stop' to datetime
    and removing duplicates.
    """
    # lowercas column name
    df.columns = df.columns.str.lower()

    # ensure 'start' and 'stop' are datetime
    df['start'] = pd.to_datetime(df['start'], errors='coerce')
    df['stop'] = pd.to_datetime(df['stop'], errors='coerce')

    # drop rows where 'start' or 'stop' could not be converted to datetime
    df = df.dropna(subset=['start', 'stop'])

    # create a surrogate key to remove duplicates
    df['surrogate_key'] = df['patient'].astype(str) + '-' + df['id'].astype(str) + '-' + df['code'].astype(str)
    df = df.drop_duplicates(subset=['surrogate_key'])

    # duration of the procedure in seconds
    df['duration_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

    # breakdown timestamp details
    df['year'] = df['start'].dt.year
    df['month'] = df['start'].dt.strftime('%B')
    df['week'] = df['start'].dt.isocalendar().week
    df['day'] = df['start'].dt.strftime('%A')

    return df

def save_cleaned_data(df: pd.DataFrame, output_path: str):
    """
    Save the cleaned data to a CSV file.
    """
    df.to_csv(output_path, index=False)

def process_data(file_path: str, output_path: str, base_cost_limit: float):
    """
    Read data from a CSV file, clean the data, exclude procedures more expensive than base_cost_limit
    """
    df = read_data(file_path)
    cleaned_df = clean_data(df)
    # exclude procedures more expensive than base_cost_limit
    cleaned_df = cleaned_df[cleaned_df['base_encounter_cost'] <= base_cost_limit]
    # drop the surrogate key column
    cleaned_df = cleaned_df.drop(columns=['surrogate_key'])

    save_cleaned_data(cleaned_df, output_path)

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    base_cost_limit = float(sys.argv[3]) if len(sys.argv) > 3 else 30000
    process_data(input_file, output_file, base_cost_limit)