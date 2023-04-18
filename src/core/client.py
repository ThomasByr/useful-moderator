import discord

from discord.ext import commands

from ..helper import *
from ..commands import *

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
    super().__init__(command_prefix=prefix, intents=intents, **options)

  @property
  def invite(self) -> str:
    return self.__invite

  async def on_ready(self):
    logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
    logger.info(f'Connected to {len(self.guilds)} guilds')
    await self.setup()
    await self.tree.sync()
    await self.change_presence(
      status=discord.Status.do_not_disturb,
      activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'v {__version__}',
      ),
    )
    logger.info('Ready !')

  async def setup(self):
    logger.info('Setting up...')

    await self.add_cog(Sudo(self))
    await self.add_cog(BotLog(self))

    await self.add_cog(Utils(self))

    logger.info('Setting up complete')
