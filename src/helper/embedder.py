import discord

from .constants import *

__all__ = [
  'build_info_embed',
  'build_response_embed',
  'build_success_embed',
  'build_fail_embed',
  'build_help_embed',
  'build_invite_embed',
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
    colour=discord.Colour.blurple(),
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


def build_fail_embed(
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
    colour=discord.Colour.blurple(),
    thumbnail=HELP_IMG,
  )


def build_invite_embed(
  title: str = None,
  description: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.blurple(),
    thumbnail=INVITE_IMG,
  )
