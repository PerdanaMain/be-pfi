from app import app
from app.config.config import Config

if __name__ == "__main__":
    port = Config.APP_PORT
    app.run(
        port=port,
        debug=True,
    )
