import psycopg2 as ps
import os
import pandas as pd
import json
import sqlite3 as sq


def get_credentials():
    # Get the credentials for psycopg2
    return {
        'dbname': os.getenv('KMS_LoL_DBNAME'),
        'user': os.getenv('KMS_LoL_USERNAME'),
        'password': os.getenv('KMS_LoL_PASSWORD'),
        'host': os.getenv('KMS_LoL_ADDRESS'),
        'port': os.getenv('KMS_LoL_PORT')
    }


# Function to get credentials and connect to sql database on AWS RDS.
# Currently not in use due to AWS RDS costs.
def get_conn_aws():
    conn = ps.connect(**get_credentials())
    cursor = conn.cursor()
    return conn, cursor


# Connect to local sqlite3 database
def get_conn_sqlite():
    conn = sq.connect('KMS_LoL.db')
    cursor = conn.cursor()
    return conn, cursor


# Create database, currently supports sqlite3
def create_database():
    # Get connection and cursor
    conn, c = get_conn_sqlite()

    c.execute('''CREATE TABLE summoner''')
