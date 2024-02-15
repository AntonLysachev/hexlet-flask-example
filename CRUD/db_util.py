import psycopg2
import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))
PATH = f"{DIR}/config_connect.json"
def get_connection():
    try:
        with open(PATH, 'r') as f:
            config = json.load(f)
        user = config['user']
        password = config['password']
        host = config['host']
        port = config['port']
        database_name = config['database_name']

        connection = psycopg2.connect(f'postgresql://{user}:{password}@{host}:{port}/{database_name}')
    except(Exception) as error : 
        print(error)

    return connection
