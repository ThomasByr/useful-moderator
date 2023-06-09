import os

from pymongo import MongoClient
from pymongo.database import Database

from .local import *
from .auto_response_data import *

from ..helper.logger import logger as log

__all__ = ['UsefulDatabase']

DB_USER = os.getenv('DB_USER', '')
DB_PASSWD = os.getenv('DB_PASSWD', '')
DB_NAME = os.getenv('DB_NAME', '')
DB_URL = os.getenv('DB_URL', '')
DB_PORT = os.getenv('DB_PORT', None)
CONNECTION_STRING = f'mongodb+srv://{DB_USER}:{DB_PASSWD}@{DB_NAME}.{DB_URL}/?retryWrites=true&w=majority'


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

  def connect(self) -> bool:
    log.debug('Connecting to database...')
    port_no = int(DB_PORT) if DB_PORT else None
    r = False
    if DB_USER != '' and DB_PASSWD != '' and DB_NAME != '' and DB_URL != '':
      self.__client = MongoClient(CONNECTION_STRING, port=port_no)
      self.__db = self.client.useful
      log.debug('Connected to database')
      r = True
    else:
      log.warning('No database credentials provided, skipping connection')
    return r

  def disconnect(self) -> bool:
    log.debug('Disconnecting from database...')
    r = False
    if self.__client is not None:
      self.__client.close()
      self.__client = None
      self.__db = None
      log.debug('Disconnected from database')
      r = True
    else:
      log.warning('No database connection to close')
    return r

  def test(self):
    log.info('Testing database connection...')
    try:
      if self.connect():
        self.db.test.insert_one({'test': 'test'})
        self.db.test.delete_one({'test': 'test'})
        self.disconnect()
      log.info('Test successful')
    except Exception as e:
      log.error(f'Test failed: {e}')

  def __enter__(self):
    self.connect()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.disconnect()
    return False

  def add_guild(self, guild: Guild):
    if not isinstance(guild, Guild):
      raise TypeError(f'Expected Guild, got {type(guild)}')
    if self.client is None:
      raise RuntimeError('Database not connected')
    guild_id = guild.id
    self.db.guilds.update_one({'id': guild_id}, {'$set': guild.to_dict()}, upsert=True)

  def get_guild(self, guild_id: int) -> Guild:
    if self.client is None:
      raise RuntimeError('Database not connected')
    guild_dict = self.db.guilds.find_one({'id': guild_id})
    if guild_dict is None:
      log.error(f'Guild {guild_id} not found in database')
      return None
    return Guild.from_dict(guild_dict)
