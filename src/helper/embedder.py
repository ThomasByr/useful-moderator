import discord

__all__ = ['build_info_embed', 'build_success_embed', 'build_fail_embed', 'build_help_embed']


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
  if footer:
    embed.set_footer(text=footer, icon_url=footer_icon)
  if thumbnail:
    embed.set_thumbnail(url=thumbnail)
  if image:
    embed.set_image(url=image)
  return embed


def build_info_embed(
  title: str = None,
  description: str = None,
  footer: str = None,
  footer_icon: str = None,
  thumbnail: str = None,
  image: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.blurple(),
    footer=footer,
    footer_icon=footer_icon,
    thumbnail=thumbnail,
    image=image,
  )


def build_response_embed(
  title: str = None,
  description: str = None,
  footer: str = None,
  footer_icon: str = None,
  thumbnail: str = None,
  image: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.gold(),
    footer=footer,
    footer_icon=footer_icon,
    thumbnail=thumbnail,
    image=image,
  )


def build_success_embed(
  title: str = None,
  description: str = None,
  footer: str = None,
  footer_icon: str = None,
  thumbnail: str = None,
  image: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.green(),
    footer=footer,
    footer_icon=footer_icon,
    thumbnail=thumbnail,
    image=image,
  )


def build_fail_embed(
  title: str = None,
  description: str = None,
  footer: str = None,
  footer_icon: str = None,
  thumbnail: str = None,
  image: str = None,
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.red(),
    footer=footer,
    footer_icon=footer_icon,
    thumbnail=thumbnail,
    image=image,
  )

def build_help_embed(
  title: str = None,
  description: str = None,
  footer: str = None,
  footer_icon: str = None,
  thumbnail: str = None,
  image: str = 'assets/images/useful_moderator.png'
) -> discord.Embed:
  return build_embed(
    title=title,
    description=description,
    colour=discord.Colour.blurple(),
    footer=footer,
    footer_icon=footer_icon,
    thumbnail=thumbnail,
    image=image,
  )
