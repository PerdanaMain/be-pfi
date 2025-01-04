from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()


def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise Exception(f"Database connection error: {str(e)}")


def get_fetch_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_FETCH_HOST"),
            database=os.getenv("DB_FETCH_NAME"),
            user=os.getenv("DB_FETCH_USERNAME"),
            password=os.getenv("DB_FETCH_PASSWORD"),
            port=os.getenv("DB_FETCH_PORT"),
        )
        return conn
    except Exception as e:
        return str(e)
