import psycopg2
from configparser import ConfigParser

def get_connection(section: str, config_path='config/database.ini'):
    parser = ConfigParser()
    parser.read(config_path)
    params = dict(parser.items(section))
    try:
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        return conn
    except psycopg2.OperationalError as e:
        return None

def test_connection(section: str, config_path='config/database.ini') -> bool:
    conn = get_connection(section, config_path)
    if conn:
        conn.close()
        return True
    return False