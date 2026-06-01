import psycopg2
from configparser import ConfigParser

def get_connection(config_path='config/database.ini'):
    parser = ConfigParser()
    parser.read(config_path)
    params = dict(parser.items('postgresql'))
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    return conn