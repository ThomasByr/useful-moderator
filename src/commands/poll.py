import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional, Callable
from typing_extensions import override

from ..helper import *
from ..helper.logger import logger as log
from ..messages import *

__all__ = ['Poll']


class MC_Pool_View(CustomView):

  def __init__(self,
               orig_inter: discord.Interaction,
               embed: discord.Embed,
               question: str,
               choices: list[str],
               allow_multiple: bool = False):
    super().__init__(orig_inter=orig_inter)
    self.embed = embed
    self.question = question
    self.choices = choices
    self.allow_multiple = allow_multiple
    self.user_choices: dict[int, set[int]] = {} # user_id: choice_id
    self.results = [0 for _ in range(len(choices))]

    for i, choice in enumerate(choices):
      self.with_new_choice(i, choice)

  @discord.ui.button(emoji=FAIL_EMOJI, label='End the poll', style=discord.ButtonStyle.danger)
  async def end_poll(self, interaction: discord.Interaction, button: discord.ui.Button):
    if not interaction.user.resolved_permissions.manage_guild:
      embed = build_error_embed(
        title='You do not have the required permissions !',
        description='You need to have the `Manage Server` permission to end the poll.',
      )
      await interaction.response.send_message(embed=embed, ephemeral=True)
      return
    self.embed.description = '**Poll has ended!**\n\n' + self.embed.description
    await interaction.response.defer()
    await self.disable_all_items()
    await self.interaction.edit_original_response(
      embed=self.embed,
      view=self,
    )

  @discord.ui.button(emoji=GEAR_EMOJI, label='Edit', style=discord.ButtonStyle.blurple)
  async def edit_poll(self, interaction: discord.Interaction, button: discord.ui.Button):
    if not interaction.user.resolved_permissions.manage_guild:
      embed = build_error_embed(
        title='You do not have the required permissions !',
        description='You need to have the `Manage Server` permission to edit the poll.',
      )
      await interaction.response.send_message(embed=embed, ephemeral=True)
      return

    embed = build_info_embed(
      title='This functionality is not implemented yet !',
      description='Please wait for a future update.',
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

  def choice_callback(self, i: int, choice: str) -> Callable[[discord.Interaction], None]:

    async def callback(interaction: discord.Interaction):
      await interaction.response.defer()
      u_choices: set[int] = set()
      try:
        u_choices = self.user_choices[interaction.user.id]
      except KeyError:
        self.user_choices[interaction.user.id] = u_choices
      if self.allow_multiple:
        if i in u_choices:
          self.results[i] -= 1
          u_choices.remove(i)
          await interaction.followup.send(f'You have removed your vote for `{choice}` !', ephemeral=True)
        else:
          self.results[i] += 1
          u_choices.add(i)
          await interaction.followup.send(f'You have voted for `{choice}` !', ephemeral=True)
      else:
        r = False
        if len(u_choices) > 0:
          self.results[list(u_choices)[0]] -= 1
          r = True
        self.results[i] += 1
        u_choices.clear()
        u_choices.add(i)
        await interaction.followup.send(
          f'You have voted for `{choice}` !{" (removed previous vote)" if r else ""}',
          ephemeral=True,
        )

      self.embed.description = '\n'.join(
        build_description_line_for_poll_embed(i, choice, self.results[i], sum(self.results))
        for i, choice in enumerate(self.choices))
      await self.interaction.edit_original_response(embed=self.embed, view=self)

    return callback

  def with_new_choice(self, i: int, choice: str) -> 'MC_Pool_View':
    return self.with_button_callback(
      emoji=NUMERIC_EMOJIS[i],
      label='0',
      custom_id=f'choice_{i}',
      callback=self.choice_callback(i, choice),
    )


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
    allow_multiple: bool = False,
  ):
    choices = [choice0, choice1, choice2, choice3, choice4, choice5, choice6, choice7, choice8, choice9]
    choices = [choice for choice in choices if choice is not None]
    if len(choices) < 2:
      embed = build_error_embed(
        title=f'{FAIL_EMOJI} not enough choices !',
        description='```You must provide at least two choices to create a poll.```',
      )
      await reply_with_status_embed(interaction, embed, failed=True)
      return
    if len(choices) > 10:
      embed = build_error_embed(
        title=f'{FAIL_EMOJI} too many choices !',
        description='```You cannot provide more than ten choices to create a poll.```',
      )
      await reply_with_status_embed(interaction, embed, failed=True)
      return

    # create the poll which will consist of an embed
    # with the question as title and the choices as fields
    # and a live view of the results
    # the footer will contain the author of the poll
    # and users will be able to vote by clicking on buttons

    # create the embed
    embed = build_poll_embed(question, choices, interaction.user, interaction.user.display_avatar)
    # create a view with the buttons
    view = MC_Pool_View(interaction, embed, question, choices, allow_multiple)
    # send the message
    await send_poll_embed(interaction, embed, view)
