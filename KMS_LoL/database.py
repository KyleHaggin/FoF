import psycopg2 as ps
import os
import pandas as pd
import json


def get_credentials():
    # Get the credentials for psycopg2
    return {
        'dbname': os.getenv('KMS_LoL_DBNAME'),
        'user': os.getenv('KMS_LoL_USERNAME'),
        'password': os.getenv('KMS_LoL_PASSWORD'),
        'host': os.getenv('KMS_LoL_ADDRESS'),
        'port': os.getenv('KMS_LoL_PORT')
    }


def get_conn():
    conn = ps.connect(**get_credentials())
    cursor = conn.cursor()
    return conn, cursor
