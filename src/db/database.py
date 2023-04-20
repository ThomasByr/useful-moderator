import os

from pymongo import MongoClient
from pymongo.database import Database

from ..helper import *

__all__ = ['UsefulDatabase']

DB_USER = os.getenv('DB_USER')
DB_PASSWD = os.getenv('DB_PASSWD')
DB_URL = os.getenv('DB_URL')
CONNECTION_STRING = f'mongodb+srv://{DB_USER}:{DB_USER}@{DB_URL}/?retryWrites=true&w=majority'


class UsefulDatabase:
  """
  ## Description
  The database class for the bot.
  """

  def __init__(self):
    self.__client: MongoClient = None
    self.__db: Database = None

  @property
  def client(self) -> MongoClient:
    return self.__client

  @property
  def db(self):
    return self.__db

  async def connect(self):
    logger.debug('Connecting to database...')
    self.__client = MongoClient(CONNECTION_STRING)
    self.__db = self.client.useful
    logger.debug('Connected to database')

  async def disconnect(self):
    logger.debug('Disconnecting from database...')
    self.__client.close()
    self.__client = None
    self.__db = None
    logger.debug('Disconnected from database')

  async def test(self):
    logger.info('Testing database connection...')
    await self.connect()
    await self.disconnect()
    logger.info('Test successful')
