import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional

from ..helper import *
from ..helper.logger import logger as log

__all__ = ['Poll']


class MC_Poll_View(discord.ui.View):
  pass


@app_commands.default_permissions(manage_guild=True)
class Poll(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot):
    self.__client = client
    log.info('Poll cog loaded !')

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = build_help_embed(
      title='Help for `Poll` group',
      description='`Poll` group contains commands that are useful for creating polls '
      ': you can create a poll with multiple choices, or a poll with only two choices (yes/no) to easily get the opinion of your members.',
    ).add_field(
      name='📊 `create`',
      value='Create a poll with multiple choices.',
      inline=False,
    ).add_field(
      name='👍 `yesno`',
      value='Create a poll with only two choices : yes or no.',
      inline=False,
    )
    await reply_with_embed(interaction, embed)

  @app_commands.command(name='create', description='Create a poll with multiple choices 📊')
  @app_commands.describe(
    question='The question of the poll',
    choice0='The first choice of the poll',
    choice1='The second choice of the poll',
    choice2='The third choice of the poll (optional)',
    choice3='The fourth choice of the poll (optional)',
    choice4='The fifth choice of the poll (optional)',
    choice5='The sixth choice of the poll (optional)',
    choice6='The seventh choice of the poll (optional)',
    choice7='The eighth choice of the poll (optional)',
    choice8='The ninth choice of the poll (optional)',
    choice9='The tenth choice of the poll (optional)',
  )
  async def create(
    self,
    interaction: discord.Interaction,
    question: str,
    choice0: str,
    choice1: str,
    choice2: Optional[str] = None,
    choice3: Optional[str] = None,
    choice4: Optional[str] = None,
    choice5: Optional[str] = None,
    choice6: Optional[str] = None,
    choice7: Optional[str] = None,
    choice8: Optional[str] = None,
    choice9: Optional[str] = None,
  ):
    choices = [choice0, choice1, choice2, choice3, choice4, choice5, choice6, choice7, choice8, choice9]
    choices = [choice for choice in choices if choice is not None]
    if len(choices) < 2:
      embed = build_error_embed(
        title=f'{FAIL_EMOJI} not enough choices !',
        description='```You must provide at least two choices to create a poll.```',
      )
      await reply_with_embed(interaction, embed)
      return
    if len(choices) > 10:
      embed = build_error_embed(
        title=f'{FAIL_EMOJI} too many choices !',
        description='```You cannot provide more than ten choices to create a poll.```',
      )
      await reply_with_embed(interaction, embed)
      return

    # create the poll which will consist of an embed
    # with the question as title and the choices as fields
    # and a live view of the results
    # the footer will contain the author of the poll
    # and users will be able to vote by clicking on buttons

    # create the embed
    embed = build_poll_embed(question, choices, interaction.user, interaction.user.display_avatar)
    # create a view with the buttons
    view = build_poll_view(choices)

    # send the message
    await send_poll_embed(interaction, embed, view)
