from aiohttp import web

from src.backend.main import app
from src.backend.utils.logging import setup_logging
from src.backend.settings import CONFIG_SERVER

def setup():
    setup_logging()
    web.run_app(
        app, 
        host=CONFIG_SERVER["host"], 
        port=CONFIG_SERVER["port"],
    )

if __name__ == "__main__":
    setup()