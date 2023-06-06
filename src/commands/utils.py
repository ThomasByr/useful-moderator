import discord
from discord import app_commands
from discord.ext import commands

from ..helper import *
from ..helper import fmt

__all__ = ['Utils']


class Utils(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot):
    self.__client = client
    fmt.info('Utils cog loaded !')

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = build_help_embed(
      title='Help for `Utils` group',
      description='`Utils` group contains commands that are useful for developers and users.',
    ).add_field(
      name='🏓 `ping`',
      value='Test my ping to Discord\'s endpoint ; will ever only fail if the bot/shard is offline.',
      inline=False,
    ).add_field(
      name='🔗 `invite`',
      value=
      'Get the bot\'s invite link. __**Note:**__ You need the `Manage Server` permission in your target server to invite the bot.',
      inline=False,
    ).add_field(
      name='⏱️ `uptime`',
      value='Get the bot\'s uptime (time since the last restart).',
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

  @app_commands.command(name='invite', description='Get the bot\'s invite link 🔗')
  async def invite(self, interaction: discord.Interaction):
    embed = build_invite_embed(
      title='Invite Link',
      description=f'Click the link below to invite me to your server!\n\n'
      f'[Invite me !]({self.__client.invite})',
    )
    # this one link exists... I swear
    await reply_with_embed(interaction, embed)

  @app_commands.command(name='uptime', description='Get the bot\'s uptime ⏱️')
  async def uptime(self, interaction: discord.Interaction):
    embed = build_response_embed(title=f'Uptime: `.:..:..` ⏱️',)
    await reply_with_embed(interaction, embed)
    uptime_: str = self.__client.uptime
    embed.title = f'Uptime: `{uptime_}` ⏱️'
    # I swear there is somewhere a `uptime` property in the client
    await edit_reply_with_embed(interaction, embed)
