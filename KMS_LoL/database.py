import psycopg2 as ps
import os
import pandas as pd
import json
import sqlite3 as sq
import riot_api


def get_credentials():
    # Get the credentials for psycopg2
    return {
        'dbname': os.getenv('KMS_LoL_DBNAME'),
        'user': os.getenv('KMS_LoL_USERNAME'),
        'password': os.getenv('KMS_LoL_PASSWORD'),
        'host': os.getenv('KMS_LoL_ADDRESS'),
        # 'port': os.getenv('KMS_LoL_PORT')
    }


# Function to get credentials and connect to sql database on AWS RDS.
# Currently not in use due to AWS RDS costs.
def get_conn():
    # Get credentials from .env
    credentials = get_credentials()
    # Print credentials for testing purposes
    print(credentials['dbname'], credentials['user'],
          credentials['password'], credentials['host'])

    # Connect to database
    conn = ps.connect(dbname=credentials['dbname'], user=credentials['user'],
                      password=credentials['password'],
                      host=credentials['host'])
    cursor = conn.cursor()

    # Return connection and cursor
    return conn, cursor


# Connect to local sqlite3 database
def get_conn_sqlite():
    conn = sq.connect('KMS_LoL.db')
    cursor = conn.cursor()
    return conn, cursor


# Create database, currently supports sqlite3
def create_database():
    # Get connection and cursor
    conn, c = get_conn()

    # Create table for summoner information if it doesn't already exist.
    create_table_summoner = """
    CREATE TABLE IF NOT EXISTS summoner (
        summoner_name VARCHAR(16),
        summoner_id VARCHAR(48),
        solo_rank_tier VARCHAR(16),
        solo_rank_rank VARCHAR(8)
    );
    """

    # Execute creation of tables
    c.execute(create_table_summoner)

    # Show tables in database
    show_tables = """
    SELECT *
    FROM pg_catalog.pg_tables
    WHERE schemaname != 'pg_catalog'
    AND schemaname != 'information_schema';
    """

    # Execute and print results of table lookup.
    c.execute(show_tables)
    print(c.fetchall())

    # Close cursor and commit connection
    c.close()
    conn.commit()


create_database()
