# Healthcare Data Pipeline
## Overview

This project demonstrates an ETL (Extract, Transform, Load) pipeline that processes healthcare data.
The pipeline extracts data from various CSV files, transforms it by cleaning and normalizing, and then loads it
into a PostgreSQL database. The project also includes data analysis queries to rank payers by costs paid,
find the top 5 highest costing patients, and the top 5 most expensive procedures on a daily basis.

## Prerequisites

- Docker
- Docker Compose
- Make

## Project Structure

```
/MightyDataEngineerTest
|-- /ETL
|   |-- /data
|   |-- /scripts
|       |-- data_cleaning.py
|       |-- data_upload.py
|       |-- create_data_marts.py
|       |-- main_etl_process.py
|       |-- queries.sql
|-- docker-compose.yaml
|-- config.yaml
|-- Makefile
```

## Setup and Running the ETL Pipeline

### 1. Clone the Repository

```
git clone https://github.com/giuliosmall/MightyDataEngineerTest.git
cd MightyDataEngineerTest
```

### 2. Prepare the Environment

Ensure Docker and Docker Compose are installed. Also, make sure Make is available on your system.

### 3. Configure Environment Variables

Ensure the environment variables are set correctly in `docker-compose.yaml`:

```
version: '3.8'
services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data
  etl:
    build:
      context: ./ETL
      dockerfile: Dockerfile
    command: python scripts/main_etl_process.py
    depends_on:
      - db
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: mydatabase
      DB_USER: user
      DB_PASSWORD: password
    volumes:
      - ./ETL/data:/app/data
      - ./ETL/scripts:/app/scripts
      - ./config.yaml:/app/config.yaml
      - ./ETL/scripts/queries.sql:/app/scripts/queries.sql
volumes:
  db-data:
```
### Security Disclaimer

All the exposed passwords and database names in this project are meant to speed up the Docker development process.
This is a practice I would never release in production. In a real-world scenario, ensure to use environment variables
or secret management tools to handle sensitive information securely.

### Data Modeling Disclaimer

This project doesn’t follow data modeling best practices like the “Medallion” approach. Here, the entire data modeling 
exercise is potentially exposed to downstream stakeholders. In a real-life scenario, this should not be the approach. 
There should be only one layer dedicated to final transformation to be exposed to Business/BI, with other layers kept 
internal to the ETL processes.

### 4. Use the Makefile

The `Makefile` provides convenient commands to manage the Docker containers.

#### Build and Run the Docker Containers

```
make
```

or

```
make all
```

#### Stop the Docker Containers

```
make down
```

#### Rebuild and Run the Docker Containers

```
make rebuild
```

#### Follow the Logs of the Docker Containers

```
make logs
```

#### Clean Up Docker Containers, Networks, and Volumes

```
make clean
```

#### Access the PostgreSQL Container

```
make psql
```

## Data Analysis

The project includes SQL queries to perform data analysis:

1. Rank Payers by Costs Paid

2. Top 5 Highest Costing Patients

3. Top 5 Most Expensive Procedures on a Daily Basis (Median)

The results of these queries are stored in the following tables:

- payer_ranking
- top_5_patients
- top_5_procedures_daily

### Example Queries to Check Results

After running the ETL process, you can check the results by accessing the PostgreSQL database:

1. Connect to the PostgreSQL Container

```
make psql
```

2. Run SQL Queries (pick one)
```
SELECT * FROM payer_ranking LIMIT 10;
SELECT * FROM top_5_patients LIMIT 10;
SELECT * FROM top_5_procedures_daily LIMIT 10;
```

## Conclusion

This project demonstrates a complete ETL pipeline using Docker, Docker Compose, and Python.
The Makefile simplifies the management of the Docker environment, making it easy to build, run, and clean up the
ETL pipeline.
