from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

import datetime

from ..helper import *

__all__ = ['BotLog']


@app_commands.default_permissions(manage_guild=True)
class BotLog(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot):
    self.__client = client
    logger.info('BotLog cog loaded !')

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = build_help_embed(
      title='Help for `BotLog` group',
      description='`BotLog` group contains commands that are useful for the bot owner.',
    ).add_field(
      name='📝 `dump`',
      value='Dump the bot log in the current channel.',
      inline=False,
    )
    await reply_with_embed(interaction, embed)

  @commands.is_owner()
  @app_commands.command(name='dump', description='Dump the bot log 📝')
  async def dump(self, interaction: discord.Interaction):
    file = discord.File('bot.log')
    failed = False
    embed = build_success_embed(title=f'{SUCCESS_EMOJI} bot log dumped !',)
    try:
      await send_channel_file(interaction.channel, file)
    except Exception as e:
      failed = True
      embed = build_fail_embed(
        title=f'{FAIL_EMOJI} bot log dump failed !',
        description=f'```{e}```',
      )
    await reply_with_status_embed(interaction, embed, failed)
