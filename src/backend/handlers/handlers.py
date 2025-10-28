import logging
import random

from aiohttp import web
from aiohttp.web_response import json_response

from src.backend.services import ServiceDatabase
from src.backend.utils.generator import gen_id

async def authenticate(request: web.Request) -> web.Response:
    db_service: ServiceDatabase = request.app["db_service"]
    data = await request.json()
    
    try:
        if data["who_is"] == "organizer":
            organizer = await db_service.get_organiser(data["login"], data["password"])
        elif data["who_is"] == "judge":
            judge = await db_service.get_judge(data["login"], data["password"])
        else:
            raise

        return json_response(
            data={
                "success": True
            },
            status=200
        )
    except Exception as error:
        logging.error("authorization error", error)

        return json_response(
            data={
                "succsess": False,
                "code": "INTERNAL_SERVER_ERROR",
                "message": "couldn't authorize"
            },
            status=400
        )

async def registration_team(request: web.Request) -> web.Response:
    db_service: ServiceDatabase = request.app["db_service"]
    data = await request.json()

    try:
        await db_service.new_team(data["name"])
        
        return json_response(
            data={
                "success": True
            },
            status=200
        )
    except Exception as error:
        logging.error("error adding the command", error)

        return json_response(
            data={
                "succsess": False,
                "code": "INTERNAL_SERVER_ERROR",
                "message": "couldn't add a command"
            },
            status=400
        )

async def registration_participant(request: web.Request) -> web.Response:
    db_service: ServiceDatabase = request.app["db_service"]
    data = await request.json()

    try:
        id = gen_id(4)
        while True:
            number = gen_id(2)
            if await db_service.check_number_of_participant(number):
                break
        team_id = await db_service.get_team_id(data["name_team"])

        if data["age"] == 12 or data["age"] == 13:
            age_group = 1
        elif data["age"] == 14 or data["age"] == 15:
            age_group = 2
        elif data["age"] == 16 or data["age"] == 17:
            age_group = 3
        elif data["age"] >= 18 and data["age"] <= 20:
            age_group = 4
        elif data["age"] >= 21 or data["age"] <= 23:
            age_group = 5
        elif data["age"] >= 24 or data["age"] <= 39:
            age_group = 6
        elif data["age"] >= 40 or data["age"] <= 49:
            age_group = 7
        elif data["age"] >= 50 or data["age"] <= 59:
            age_group = 8
        elif data["age"] >= 60 or data["age"] <= 69:
            age_group = 9
        elif data["age"] >= 70 or data["age"] <= 79:
            age_group = 10
        elif data["age"] >= 80:
            age_group = 11

        await db_service.new_participant(
            id,
            data["first_name"],
            data["second_name"],
            data["patronymic"],
            data["age"],
            age_group,
            number,
            team_id
            )
        
        return json_response(
            data={
                "success": True,
                "number": number
            },
            status=200
        )
    except Exception as error:
        logging.error("error adding the command", error)

        return json_response(
            data={
                "succsess": False,
                "code": "INTERNAL_SERVER_ERROR",
                "message": "couldn't add a command"
            },
            status=400
        )
    
async def start_competition(request: web.Request) -> web.Response:
    db_service: ServiceDatabase = request.app["db_service"]

    try:
        participants = await db_service.get_all_participants()
        random.shuffle(participants)

        return json_response(
            data={
                "success": True,
                "participants": participants
            },
            status=200
        )
    except Exception as error:
        logging.error("error starting the competition", error)

        return json_response(
            data={
                "succsess": False,
                "code": "INTERNAL_SERVER_ERROR",
                "message": "couldn't add a command"
            },
            status=400
        )