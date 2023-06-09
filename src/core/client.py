import os
import signal
import sys

import discord

from typing_extensions import override
from discord.ext import commands

import datetime

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

    log.info('Messing around ...')
    await self.tree.sync()
    await self.change_presence(
      status=discord.Status.do_not_disturb,
      activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'v {__version__}',
      ),
    )
    self.__db.test()

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
    log.info('Shutdown complete')
    sys.exit(0)

  async def setup(self):
    log.info('Setting up...')

    await self.add_cog(Sudo(self))
    await self.add_cog(BotLog(self))

    await self.add_cog(Utils(self))
    await self.add_cog(Poll(self))

    log.info('Setting up complete')
