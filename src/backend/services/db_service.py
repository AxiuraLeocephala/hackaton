import asyncio
from typing import Dict

from src.backend.db import InterfaceDatabase
from src.backend.patterns import Singleton
from src.backend.utils.generator import gen_id

class ServiceDatabase(Singleton):
    __db: InterfaceDatabase = None 

    def __init__(self, db: InterfaceDatabase):
        self.__db = db
    
    async def get_organiser(self, login, password):
        organiser = await self.__db.query(f"SELECT * FROM `organizer` WHERE Login={login} AND Password={password}")
        return organiser

    
    async def get_judge(self, login, password):
        judge = await self.__db.query(f"SELECT * FROM `judge` WHERE Login={login} AND Password={password}")
        return judge
    
    async def new_team(self, name):
        id = gen_id(4)
        await self.__db.execute(f"INSERT INTO `team` (ID, Name) VALUES ('{id}', '{name}')")

    async def check_number_of_participant(self, number):
        participant_id = await self.__db.query(f"SELECT ID FROM `participant` WHERE Number={number}")
        return True if participant_id else False

    async def get_team_id(self, name):
        id = await self.__db.query(f"SELECT ID FROM `team` WHERE Name='{name}'")
        return id[0][0]

    async def new_participant(
            self,
            id,
            first_name,
            second_name,
            patronymic,
            age,
            age_group,
            number,
            team_id
        ):
        await self.__db.query(
            "INSERT INTO `participant` " \
            "(ID, FirstName, SecondName, Patronymic, Age, AgeGroup, Number, Team)" \
            f"VALUES ({id}, '{first_name}', '{second_name}', '{patronymic}', {age}, {age_group}, {number}, {team_id})"
        )

    async def get_all_participants(self):
        participants = await self.__db.query("SELECT ID, Number FROM `participant`")
        
        return participants