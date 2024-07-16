import os
import subprocess


def substitute_config_placeholders():
    with open("/app/config.yaml", "r") as file:
        config = file.read()

    config = config.replace("${DB_USER}", os.getenv("DB_USER", "user"))
    config = config.replace("${DB_PASSWORD}", os.getenv("DB_PASSWORD", "password"))
    config = config.replace("${DB_HOST}", os.getenv("DB_HOST", "db"))
    config = config.replace("${DB_PORT}", os.getenv("DB_PORT", "5432"))
    config = config.replace("${DB_NAME}", os.getenv("DB_NAME", "mydatabase"))

    with open("/app/config.yaml", "w") as file:
        file.write(config)


def main():
    substitute_config_placeholders()

    # Step 1: Clean the data
    subprocess.run(
        ["python", "scripts/data_cleaning.py", "/app/data/encounters.csv", "/app/data/encounters_cleaned.csv", "30000"])

    # Step 2: Upload cleaned data to PostgreSQL
    subprocess.run(["python", "scripts/data_upload.py"])

    # Step 3: Create data marts
    subprocess.run(["python", "scripts/create_data_marts.py"])


if __name__ == "__main__":
    main()