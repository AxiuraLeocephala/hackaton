from typing import Iterable 

from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef

from src.backend.handlers.handlers import * 

def setup_routes(app: web.Application) -> Iterable[AbstractRouteDef]:
    routes_table = [
        web.post("/authenticate", authenticate),
        web.post("/registration_team", registration_team),
        web.post("/registration_participant", registration_participant),
        web.post("/start_competition", start_competition)
    ]

    app.add_routes(routes_table)