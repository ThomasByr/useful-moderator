import os

from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

import re
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

  @commands.is_owner()
  @app_commands.command(name='filter', description='Filter the bot log based on some expressions 🔎')
  @app_commands.describe(
    expressions='Words or regex expressions (csv) to filter the bot log with',
    mode='Mode of the filter (all or any))',
  )
  @app_commands.choices(
    mode=[app_commands.Choice(name='all', value=0),
          app_commands.Choice(name='any', value=1)])
  async def filter(self, interaction: discord.Interaction, expressions: str, mode: app_commands.Choice[int]):
    expressions: list[str] = expressions.split(',')
    expressions = list(map(lambda expression: expression.strip().lower(), expressions))
    embed = build_success_embed(
      title=f'{SUCCESS_EMOJI} bot log filtered !',
      description=f'```{mode.name}\n{expressions}```',
    )
    failed = False
    try:
      # there are so many things that can go wrong here...
      # todo: better logging lines parsing (maybe cut before the timestamp)
      with open('bot.log', 'r') as f:
        lines = f.readlines()
      if mode.value == 0:
        lines = [
          line for line in lines if all(re.search(expression, line.lower()) for expression in expressions)
        ]
      else:
        lines = [
          line for line in lines if any(re.search(expression, line.lower()) for expression in expressions)
        ]
      with open('tmp.bot.log', 'w') as f:
        f.writelines(lines)
      file = discord.File('tmp.bot.log')
      await send_channel_file(interaction.channel, file)
      os.remove('tmp.bot.log')
    except Exception as e:
      failed = True
      embed = build_fail_embed(
        title=f'{FAIL_EMOJI} bot log filter failed !',
        description=f'```{e}```',
      )
    await reply_with_status_embed(interaction, embed, failed)
