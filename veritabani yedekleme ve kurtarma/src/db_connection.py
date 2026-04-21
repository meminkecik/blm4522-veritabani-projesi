import psycopg2
from configparser import ConfigParser
import os


def config(filename='config/database.ini', section='postgresql'):
    if not os.path.isfile(filename):
        raise Exception(f"{filename} dosyası bulunamadı!")

    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    return db


def connect():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        return conn
    except Exception as error:
        print(f"Bağlantı hatası: {error}")
        return None