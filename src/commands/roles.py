from collections.abc import Callable
from typing import Optional
from typing_extensions import override

import discord
from discord import app_commands
from discord.ext import commands

from ..helper import *
from ..helper.logger import logger as log
from ..messages import *

__all__ = ['Roles']


# pylint: disable=all
@app_commands.default_permissions(administrator=True)
class Roles(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot):
    self.__client = client # pylint: disable=unused-private-member
    log.info('Roles cog loaded !')

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = build_help_embed(
      title='Help for `Roles` group',
      description='`Roles` group contains commands that are useful for guild admins.',
    )
