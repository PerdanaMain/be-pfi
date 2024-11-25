import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PORT = os.getenv("APP_PORT")
    AUTH_SERVICE_ENDPOINT = os.getenv("AUTH_SERVICE_ENDPOINT")

    DB_MAIN_HOST = os.getenv("DB_MAIN_HOST", "192.168.1.82")
    DB_MAIN_NAME = os.getenv("DB_MAIN_NAME", "digital_twin")
    DB_MAIN_USERNAME = os.getenv("DB_MAIN_USERNAME", "postgres")
    DB_MAIN_PASSWORD = os.getenv("DB_MAIN_PASSWORD", "postgres")
    DB_MAIN_PORT = os.getenv("DB_MAIN_PORT", 5432)

    DB_FETCH_HOST = os.getenv("DB_FETCH_HOST")
    DB_FETCH_NAME = os.getenv("DB_FETCH_NAME")
    DB_FETCH_USERNAME = os.getenv("DB_FETCH_USERNAME")
    DB_FETCH_PASSWORD = os.getenv("DB_FETCH_PASSWORD")
    DB_FETCH_PORT = os.getenv("DB_FETCH_PORT", 5432)

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_MAIN_USERNAME}:{DB_MAIN_PASSWORD}@{DB_MAIN_HOST}:{DB_MAIN_PORT}/{DB_MAIN_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
