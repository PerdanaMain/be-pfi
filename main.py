from app import app
from config import Config

if __name__ == "__main__":
    port = Config.PORT
    app.run(
        port=port,
        debug=True,
    )
