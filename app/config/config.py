from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    AUTH_SERVICE_ENDPOINT = os.getenv("AUTH_SERVICE_ENDPOINT")
    APP_PORT = os.getenv("APP_PORT")

    PIWEB_API_URL = os.getenv("PIWEB_API_URL")
    PIWEB_API_USER = os.getenv("PIWEB_API_USER")
    PIWEB_API_PASS = os.getenv("PIWEB_API_PASS")

    DB_FETCH_HOST = os.getenv("DB_FETCH_HOST")
    DB_FETCH_USER = os.getenv("DB_FETCH_USER")
    DB_FETCH_PASS = os.getenv("DB_FETCH_PASS")
    DB_FETCH_NAME = os.getenv("DB_FETCH_NAME")
    DB_FETCH_PORT = os.getenv("DB_FETCH_PORT")

    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = os.getenv("DB_PORT")

    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
    UPLOAD_FOLDER = "public/uploads/equipments"
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
