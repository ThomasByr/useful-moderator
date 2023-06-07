import discord

from ..helper.constants import *

__all__ = [
  'build_info_embed',
  'build_response_embed',
  'build_success_embed',
  'build_error_embed',
  'build_help_embed',
  'build_invite_embed',
  'build_description_line_for_poll_embed',
  'build_description_line_for_yesno_poll_embed',
  'build_poll_embed',
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


def build_description_line_for_poll_embed(i: int, choice: str, votes: int, total_votes: int) -> str:
  width = 10
  if total_votes > 0:
    progress = int(votes / total_votes * width)
  else:
    progress = 0
  return f'{NUMERIC_EMOJIS[i]} {choice}\n`{"█" * progress + " " * (width - progress)}` ({votes})\n'


def build_description_line_for_yesno_poll_embed(i: int, votes: int, total_votes: int) -> str:
  width = 10
  if total_votes > 0:
    progress = int(votes / total_votes * width)
  else:
    progress = 0
  return f'{YESNO_EMOJIS[i]} {("YES", "NO")[i]}\n`{"█" * progress + " " * (width - progress)}` ({votes})\n'


def build_poll_embed(
  title: str = None,
  choices: list[str] = None,
  author: str = None,
  author_icon: str = None,
) -> discord.Embed:
  if 'Yes' in choices and 'No' in choices:
    return build_embed(
      title=title,
      description='\n'.join(
        [build_description_line_for_yesno_poll_embed(i, 0, 0) for i, choice in enumerate(choices)]),
      thumbnail=VOTE_IMG,
      colour=discord.Colour.gold(),
      footer=author,
      footer_icon=author_icon,
    )
  return build_embed(
    title=title,
    description='\n'.join(
      [build_description_line_for_poll_embed(i, choice, 0, 0) for i, choice in enumerate(choices)]),
    thumbnail=VOTE_IMG,
    colour=discord.Colour.gold(),
    footer=author,
    footer_icon=author_icon,
  )
