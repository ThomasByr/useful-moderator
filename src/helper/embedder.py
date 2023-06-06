import discord

from .constants import *

__all__ = [
  'build_info_embed',
  'build_response_embed',
  'build_success_embed',
  'build_error_embed',
  'build_help_embed',
  'build_invite_embed',
  'build_poll_embed',
  'build_poll_view',
]

#%% base embedder


def build_embed(
  title: str = None,
  description: str = None,
  colour: discord.Colour = discord.Colour.blurple(),
  footer: str = None,
  footer_icon: str = None,
  thumbnail: str = None,
  image: str = None,
) -> discord.Embed:
  embed = discord.Embed(
    title=title,
    description=description,
    colour=colour,
  )
  if footer is not None:
    embed.set_footer(text=footer, icon_url=footer_icon)
  if thumbnail is not None:
    embed.set_thumbnail(url=thumbnail)
  if image is not None:
    embed.set_image(url=image)
  return embed


#%% custom embedder


def build_info_embed(
  title: str = None,
  description: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
  )


def build_response_embed(
  title: str = None,
  description: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.gold(),
  )


def build_success_embed(
  title: str = None,
  description: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.green(),
  )


def build_error_embed(
  title: str = None,
  description: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.red(),
    thumbnail=FAIL_IMG,
  )


def build_help_embed(
  title: str = None,
  description: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    thumbnail=HELP_IMG,
  )


def build_invite_embed(
  title: str = None,
  description: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    thumbnail=INVITE_IMG,
  )


def build_poll_embed(
  title: str = None,
  choices: list[str] = None,
  author: str = None,
  author_icon: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description='\n'.join([f'{NUMERIC_EMOJIS[i]} {choice}' for i, choice in enumerate(choices)]),
    thumbnail=VOTE_IMG,
    colour=discord.Colour.gold(),
    footer=author,
    footer_icon=author_icon,
  )


def build_poll_view(choices: list[str] = None,) -> discord.ui.View:
  view = discord.ui.View()
  for i, _ in enumerate(choices):
    view.add_item(discord.ui.Button(custom_id=f'poll_{i}', emoji=NUMERIC_EMOJIS[i]))
  return view
