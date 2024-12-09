from dotenv import load_dotenv
import os


class Config:
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    AUTH_SERVICE_ENDPOINT = os.getenv("AUTH_SERVICE_ENDPOINT")
    APP_PORT = os.getenv("APP_PORT")
