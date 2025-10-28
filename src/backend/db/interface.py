from abc import ABC, abstractmethod
from typing import Dict, Union, List, Tuple

from mysql.connector import cursor, pooling

class InterfaceDatabase(ABC):
    @abstractmethod
    async def query(
        self, 
        sql: str, params: Union[List, Tuple] = None,
        cnx: Union[pooling.PooledMySQLConnection] = None, cursor: Union[cursor.MySQLCursor] = None
    ) -> Union[Tuple, Dict, None]: pass

    @abstractmethod
    async def execute(
        self, 
        sql: str, params: Union[List, Tuple] = None,
        cnx: Union[pooling.PooledMySQLConnection] = None, cursor: Union[cursor.MySQLCursor] = None
    ) -> None: pass