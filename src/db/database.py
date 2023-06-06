import os

from pymongo import MongoClient
from pymongo.database import Database

from ..helper.logger import logger as log

__all__ = ['UsefulDatabase']

DB_USER = os.getenv('DB_USER', '')
DB_PASSWD = os.getenv('DB_PASSWD', '')
DB_URL = os.getenv('DB_URL', '')
DB_PORT = os.getenv('DB_PORT', None)
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

  def connect(self):
    log.debug('Connecting to database...')
    port_no = int(DB_PORT) if DB_PORT else None
    if DB_USER != '' and DB_PASSWD != '' and DB_URL != '':
      self.__client = MongoClient(CONNECTION_STRING, port=port_no)
      self.__db = self.client.useful
      log.debug('Connected to database')
    else:
      log.warning('No database credentials provided, skipping connection')

  def disconnect(self):
    log.debug('Disconnecting from database...')
    if self.__client is not None:
      self.__client.close()
      self.__client = None
      self.__db = None
      log.debug('Disconnected from database')
    else:
      log.warning('No database connection to close')

  def test(self):
    log.info('Testing database connection...')
    try:
      self.connect()
      self.disconnect()
      log.info('Test successful')
    except Exception as e:
      log.error(f'Test failed: {e}')
