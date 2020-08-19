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


# Function to get credentials and connect to sql database on ElephantSQL.
def get_conn():
    # Get credentials from .env
    credentials = get_credentials()

    # Try/Except to connect to database, throw error if failed.
    try:
        # Connect to database
        conn = ps.connect(dbname=credentials['dbname'],
                          user=credentials['user'],
                          password=credentials['password'],
                          host=credentials['host'])
        cursor = conn.cursor()
    except Error as e:
        print(e)

    # Return connection and cursor
    return conn, cursor


# Connect to local sqlite3 database
def get_conn_sqlite():
    conn = sq.connect('KMS_LoL.db')
    cursor = conn.cursor()
    return conn, cursor


# Create database, currently supports ElephantSQL
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

    # Close cursor and commit connection
    c.close()
    conn.commit()


def insert_summoner_information(summoner_name):
    # Get connection and cursor
    conn, c = get_conn()

    summoner, summoner_ranked = riot_api.summoner_information(summoner_name)

    insert_info = (summoner['name'], summoner['id'],
                   summoner_ranked[1]['tier'], summoner_ranked[1]['rank'])

    insert_summoner_info = """
    INSERT INTO summoner
    (summoner_name, summoner_id, solo_rank_tier, solo_rank_rank)
    VALUES (%s, %s, %s, %s)"""

    try:
        c.execute(insert_summoner_info, insert_info)
    except Error as e:
        print(e)
    finally:
        # Close cursor and commit connection
        c.close()
        conn.commit()


def read_summoner_information(summoner_name):
    get_summoner_info = """
    SELECT * FROM summoner WHERE summoner_name='{}'
    """.format(str(summoner_name))

    # try:
    # Get connection and cursor
    conn, c = get_conn()

    # Execute select request from SQL database.
    c.execute(get_summoner_info)

    info_recieved = c.fetchall()

    print(info_recieved)
    # except Error as e:
    #     print(e)
    # finally:
    #     # Close cursor and commit connection
    #     c.close()
    #     conn.commit()


# Execute database creation and summoner information insert if file is run.
if __name__ == "__main__":
    create_database()
    insert_summoner_information('Rârgh')
    read_summoner_information('Rârgh')
