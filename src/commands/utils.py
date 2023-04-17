import discord
from discord import app_commands
from discord.ext import commands

from ..helper import *

__all__ = ['Utils']


class Utils(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot):
    self.__client = client
    logger.info('Utils cog loaded !')

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = build_help_embed(
      title='Help for `Utils` group',
      description='`Utils` group contains commands that are useful for developers and users.',
    ).add_field(
      name='🏓 `ping`',
      value='Test my ping to Discord\'s endpoint ; will ever only fail if the bot/shard is offline.',
      inline=False,
    )
    await reply_with_embed(interaction, embed)

  @app_commands.command(name='ping', description='Test my ping to Discord\'s endpoint 🏓')
  async def ping(self, interaction: discord.Interaction):
    embed = build_response_embed(title=f'Pong! `...ms` 🏓',)
    await reply_with_embed(interaction, embed)
    ping_ = f'{round(self.__client.latency * 1000)}ms'
    embed.title = f'Pong! `{ping_}` 🏓'
    await edit_reply_with_embed(interaction, embed)
