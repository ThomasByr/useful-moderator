import discord
from discord import app_commands
from discord.ext import commands

from ..helper import build_info_embed, build_help_embed, logger

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
      name='`ping`',
      value='Test my ping to Discord\'s endpoint',
      inline=False,
    )
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name='ping', description='Test my ping to Discord\'s endpoint')
  async def ping(self, interaction: discord.Interaction):
    ping_ = f'{round(self.__client.latency * 1000)}ms'
    embed = build_info_embed(
      title='Pong!',
      description=f'`{ping_}`',
    )
    await interaction.response.send_message(embed=embed)
