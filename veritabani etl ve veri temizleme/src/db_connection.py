import psycopg2
from configparser import ConfigParser

def get_connection(config_path='config/database.ini'):
    parser = ConfigParser()
    parser.read(config_path)
    params = dict(parser.items('postgresql'))
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    return conn

def get_sqlalchemy_engine(config_path='config/database.ini'):
    from sqlalchemy import create_engine
    parser = ConfigParser()
    parser.read(config_path)
    p = dict(parser.items('postgresql'))
    url = f"postgresql+psycopg2://{p['user']}@{p['host']}/{p['database']}"
    return create_engine(url)