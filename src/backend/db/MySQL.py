import logging
from typing import Dict, List, Union, Tuple
from contextlib import contextmanager

import mysql.connector as mysql_connector
from mysql.connector import cursor, pooling

from src.backend.db import InterfaceDatabase
from src.backend.patterns import Singleton

class MySQL(InterfaceDatabase, Singleton):
    __pool: pooling.MySQLConnectionPool
    __counter_of_available_connections: list

    def __init__(
            self, 
            pool: pooling.MySQLConnectionPool,
            counter_of_available_connections: List
        ):
        self.__pool = pool
        self.__counter_of_available_connections = counter_of_available_connections

    def __get_connection_from_pool(self) -> Tuple[pooling.PooledMySQLConnection, cursor.MySQLCursor]:
        try:
            cnx = self.__pool.get_connection()
            cursor = cnx.cursor()
            self.__counter_of_available_connections[0] -= 1
            return cnx, cursor
        except mysql_connector.Error as mysql_error:
            logging.error("error getting connection from pool:", mysql_error)
            raise

    def __close_connection_from_pool(
            self, 
            cnx: pooling.PooledMySQLConnection, cursor: cursor.MySQLCursor
            ) -> None:
        try:
            cursor.close()
            cnx.close()
            self.__counter_of_available_connections[0] += 1
        except Exception as mysql_error:
            logging.error("error closing connection:", mysql_error)
            raise

    async def query(
            self, 
            sql: str, params: Union[List, Tuple] = None,
            cnx: Union[pooling.PooledMySQLConnection] = None, cursor: Union[cursor.MySQLCursor] = None
        ) -> Union[Tuple, Dict, None]:
        in_transaction = True

        if not(cnx and cursor):
            in_transaction = False
            cnx, cursor = self.__get_connection_from_pool()

        try:
            cursor.execute(operation=sql, params=params)
            result = cursor.fetchall()
            
            return result
        except mysql_connector.Error as mysql_error:
            logging.error("failed to complete the query: ", mysql_error)
            raise
        finally:
            if not in_transaction:
                self.__close_connection_from_pool(cnx, cursor)

    async def execute(
            self, 
            sql: str, params: Union[List, Tuple] = None,
            cnx: Union[pooling.PooledMySQLConnection] = None, cursor: Union[cursor.MySQLCursor] = None
        ) -> None:
        in_transaction = True

        if not(cnx and cursor):
            in_transaction = False
            cnx, cursor = self.__get_connection_from_pool()
        
        try:
            result = cursor.execute(operation=sql, params=params)
            cnx.commit()
        except mysql_connector.Error as mysql_error:
            logging.error("error execution query: ", mysql_error)
            raise
        finally:
            if not in_transaction:
                self.__close_connection_from_pool(cnx, cursor)

    @contextmanager
    def transaction(self):
        cnx, cursor = self.__get_connection_from_pool()
        self.__counter_of_available_connections[0] -= 1
        try:
            cnx.start_transaction()
            yield cnx, cursor
            cnx.commit()
        except:
            cnx.rollback()
            raise
        finally:
            cursor.close()
            cnx.close()
            self.__counter_of_available_connections[0] += 1