from config import Config
import psycopg2


def get_connection():
    try:
        conn = psycopg2.connect(
            host=Config.DB_MAIN_HOST,
            database=Config.DB_MAIN_NAME,
            user=Config.DB_MAIN_USERNAME,
            password=Config.DB_MAIN_PASSWORD,
            port=Config.DB_MAIN_PORT,
        )
        return conn
    except Exception as e:
        return str(e)


def get_fetch_connection():
    try:
        conn = psycopg2.connect(
            host=Config.DB_FETCH_HOST,
            database=Config.DB_FETCH_NAME,
            user=Config.DB_FETCH_USERNAME,
            password=Config.DB_FETCH_PASSWORD,
            port=Config.DB_FETCH_PORT,
        )
        return conn
    except Exception as e:
        return str(e)
