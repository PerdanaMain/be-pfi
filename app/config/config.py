from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    AUTH_SERVICE_ENDPOINT = os.getenv("AUTH_SERVICE_ENDPOINT")
    APP_PORT = os.getenv("APP_PORT")
