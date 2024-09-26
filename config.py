import os


class Config:
    PORT = os.getenv("APP_PORT")
    AUTH_SERVICE_ENDPOINT = os.getenv("AUTH_SERVICE_ENDPOINT")

    DB_HOST = "192.168.1.51"
    DB_NAME = os.getenv("DB_NAME", "digital_twin")
    DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_PORT = os.getenv("DB_PORT", 5433)

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
