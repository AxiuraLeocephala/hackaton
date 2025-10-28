import logging
import time
from typing import Dict, List

import mysql.connector as mysql_connector
from mysql.connector import pooling, errorcode

from src.backend.db import MySQL
from src.backend.patterns import Singleton
from src.backend.settings import CONFIG_DATABASE

class ManagerDatabase(Singleton):
    __pool: pooling.MySQLConnectionPool = None
    __config: Dict = None
    __number_of_available_connections: List
    __counter_of_available_connections: List

    __INTERVAL_BETWEEB_CHEKING_THE_NUMBER_OF_AVAIBLE_CONNECTIONS = 10 # seconds
    __NUMBER_OF_CHEKS_ON_THE_NUMBER_OF_FREE_CONNECTIONS = 10

    def __init__(self):
        self.__config = CONFIG_DATABASE
        self.__number_of_available_connections = [CONFIG_DATABASE["pool_size"]]
        self.__counter_of_available_connections = self.__number_of_available_connections

    def init(self) -> MySQL:
        try:
            self.__pool = pooling.MySQLConnectionPool(**self.__config)
            logging.info("succsessful creation of a connection pool")
            return MySQL(
                self.__pool,
                self.__counter_of_available_connections
            )
        except mysql_connector.Error as mysql_error:
            match mysql_error.errno:
                case errorcode.ER_ACCESS_DENIED_ERROR:
                    logging.error("comeone os wrong woth your username or password")
                case errorcode.ER_BAD_DB_ERROR:
                    logging.error("database does not exist")
                case _:
                    logging.error("error connection to database:", mysql_error.msg) 
            raise

    def close(self) -> None:
        for _ in range(self.__NUMBER_OF_CHEKS_ON_THE_NUMBER_OF_FREE_CONNECTIONS):
            if self.__counter_of_available_connections[0] == self.__number_of_available_connections[0]:
                self.__pool = None
                logging.info("successfully closing the connection pool")
                break
            else:
                time.sleep(self.__INTERVAL_BETWEEB_CHEKING_THE_NUMBER_OF_AVAIBLE_CONNECTIONS)
        else:
            logging.warning("exceeded the number of checks on the number " \
            "of free connections, forced disconnection from databases")
            self.__pool = None