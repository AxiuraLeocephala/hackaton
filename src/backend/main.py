from aiohttp import web

from src.backend.db import ManagerDatabase
from src.backend.services import ServiceDatabase
from src.backend.routes import setup_routes
from src.backend.middlewares.cors import add_cors_to

async def on_shutdown(app):
    app["db_manager"].close()

app = web.Application()

app["db_manager"] = ManagerDatabase()
db = app["db_manager"].init()
app["db_service"] = ServiceDatabase(db)

setup_routes(app)
add_cors_to(app)

app.on_shutdown.append(on_shutdown)