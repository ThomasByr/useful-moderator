import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional

from ..helper import *
from ..helper.logger import logger as log

__all__ = ['AutoResponse']


@app_commands.default_permissions(manage_guild=True)
class AutoResponse(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot):
    self.__client = client
    log.info('AutoResponse cog loaded !')
