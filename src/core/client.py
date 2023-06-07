import os
import signal
import sys

import discord

from typing_extensions import override
from discord.ext import commands

import datetime
import pickle

from ..helper import *
from ..helper import logger
from ..helper.logger import logger as log
from ..commands import *
from ..db import *

from ..version import __version__

__all__ = ['UsefulClient']


class UsefulClient(commands.AutoShardedBot):
  """
  ## Description
  The client class for the bot.
  """

  def __init__(self, prefix: str = '!', invite: str = None, **options):
    intents = discord.Intents.all()
    self.__invite = invite
    self.__start_time = datetime.datetime.now()
    super().__init__(command_prefix=prefix, intents=intents, **options)

    self.__db = UsefulDatabase()
    self.__local_user_db: dict[Snowflake, User] = {}
    self.__local_guild_db: dict[Snowflake, Guild] = {}

  @property
  def invite(self) -> str:
    return self.__invite

  @property
  def uptime(self) -> str:
    return str(datetime.datetime.now() - self.__start_time).split('.')[0]

  @property
  def start_time(self) -> float:
    return self.__start_time.timestamp()

  @override
  async def on_ready(self):
    log.info(f'Logged in as {self.user} (ID: {self.user.id})')
    log.info(f'Connected to {len(self.guilds)} guilds')
    await self.setup()
    await self.tree.sync()
    await self.change_presence(
      status=discord.Status.do_not_disturb,
      activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'v {__version__}',
      ),
    )
    log.info('Messing around ...')
    self.__db.test()

    self.load_locals()
    signal.signal(signal.SIGINT, self.on_end_handler)
    signal.signal(signal.SIGTERM, self.on_end_handler)

    log.info('Ready 🥳 !')

  @override
  def run(self, token: str) -> None:
    """
    Runs the bot.

    ## Parameters
    ```py
    >>> token : str
    ```
    The bot token.
    """
    super().run(
      token,
      reconnect=True,
      log_handler=logger.console_handler,
      log_formatter=logger.default_formatter,
      log_level=logger.log_lvl,
    )

  def on_end_handler(self, sig: int, frame) -> None:
    """
    Synchronously shuts down the bot.

    ## Parameters
    ```py
    >>> sig : int
    ```
    The signal number.
    ```py
    >>> frame : Frame
    ```
    The frame object.
    """
    print('', end='\r')
    log.info('Shutting down...')
    self.__db.disconnect()
    self.save_locals()
    log.info('Shutdown complete')
    sys.exit(0)

  def load_locals(self) -> None:
    """
    Loads the local user and guild database from the pickle file.\\
    Searches for the files in the `data` directory.
    """
    if not os.path.exists('data'):
      os.mkdir('data')

    try:
      with open(os.path.join('data', 'local_guild_db.pickle'), 'rb') as f:
        self.__local_user_db = pickle.load(f)
    except FileNotFoundError:
      log.warning('Local user database not found, creating new one')
      with open(os.path.join('data', 'local_user_db.pickle'), 'wb') as f:
        pickle.dump({}, f)

    try:
      with open(os.path.join('data', 'local_guild_db.pickle'), 'rb') as f:
        self.__local_guild_db = pickle.load(f)
    except FileNotFoundError:
      log.warning('Local guild database not found, creating new one')
      with open(os.path.join('data', 'local_guild_db.pickle'), 'wb') as f:
        pickle.dump({}, f)

  def save_locals(self) -> None:
    """
    Saves the local user and guild database to the pickle file.\\
    Saves the files in the `data` directory.
    """
    with open(os.path.join('data', 'local_user_db.pickle'), 'wb') as f:
      pickle.dump(self.__local_user_db, f)
    with open(os.path.join('data', 'local_guild_db.pickle'), 'wb') as f:
      pickle.dump(self.__local_guild_db, f)

  async def setup(self):
    log.info('Setting up...')

    await self.add_cog(Sudo(self))
    await self.add_cog(BotLog(self))

    await self.add_cog(Utils(self))
    await self.add_cog(Poll(self))

    log.info('Setting up complete')
