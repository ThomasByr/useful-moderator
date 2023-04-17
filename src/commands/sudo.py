from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

import datetime

from ..helper import *

__all__ = ['Sudo']


@app_commands.default_permissions(manage_guild=True)
class Sudo(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot):
    self.__client = client
    logger.info('Sudo cog loaded !')

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = build_help_embed(
      title='Help for `Sudo` group',
      description='`Sudo` group contains commands that are useful for developers and users.',
    ).add_field(
      name='`echo` 🤫',
      value='Echo a message as the bot.',
    ).add_field(
      name='`timeout` 🔨',
      value='Timeout a specific user for a given duration (reason is optional).',
    )
    await reply_with_embed(interaction, embed)

  @app_commands.command(name='echo', description='Echo a message 🤫')
  async def echo(self, interaction: discord.Interaction, message: str):
    embed = build_success_embed(title=f'{SUCCESS_EMOJI} message sent !',)
    failed = False
    try:
      await send_channel_message(interaction.channel, message)
    except Exception as e:
      failed = True
      embed = build_fail_embed(
        title=f'{FAIL_EMOJI} error while sending message !',
        description=f'```{e}```',
      )
    await reply_with_status_embed(interaction, embed, failed)

  @app_commands.command(name='timeout', description='Timeout a user 🔨')
  @app_commands.describe(duration='Duration of the timeout', reason='Reason for the timeout (optional)')
  @app_commands.choices(duration=[app_commands.Choice(name='1 minute', value=60), app_commands.Choice(name='1 hour', value=3600), app_commands.Choice(name='6 hours', value=21600), app_commands.Choice(name='1 day', value=86400), app_commands.Choice(name='1 week', value=604800), app_commands.Choice(name='3 weeks', value=1814400)])
  async def timeout(
    self,
    interaction: discord.Interaction,
    user: discord.Member,
    duration: app_commands.Choice[int],
    reason: Optional[str] = None,
  ):
    embed = build_success_embed(
      title=f'{SUCCESS_EMOJI} user `{user}` has been timed out for `{duration.name}` !',
    )
    failed = False
    try:
      delta = datetime.timedelta(seconds=duration.value)
      await user.timeout(delta, reason=reason)
    except Exception as e:
      failed = True
      embed = build_fail_embed(
        title=f'{FAIL_EMOJI} error while timing out user `{user}` !',
        description=f'```{e}```',
      )
    await reply_with_status_embed(interaction, embed, failed)
