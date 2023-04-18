from typing import Any, Coroutine
import discord

__all__ = [
  'reply_with_embed',
  'edit_reply_with_embed',
  'reply_with_status_embed',
  'send_channel_message',
  'send_channel_file',
]


#%% base functions
def send_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
  ephemeral: bool = False,
  delete_after: float = None,
):
  return interaction.response.send_message(embed=embed, ephemeral=ephemeral, delete_after=delete_after)


def edit_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
):
  return interaction.edit_original_response(embed=embed)


#%% custom functions


def reply_with_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
) -> Coroutine[Any, Any, None]:
  """
  reply the sender with an embed

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  return send_embed(interaction, embed)


def edit_reply_with_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
) -> Coroutine[Any, Any, None]:
  """
  edit the reply with an embed

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  return edit_embed(interaction, embed)


def reply_with_status_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
  failed: bool = False,
) -> Coroutine[Any, Any, None]:
  """
  reply the sender with a status embed

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send
  ```py
  >>> failed : bool, (optional)
  ```
  if the request failed (if the request failed, the embed won't be automatically deleted)\\
  defaults to `False`

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  return send_embed(interaction, embed, ephemeral=True, delete_after=5 if not failed else None)


def send_channel_message(channel: discord.TextChannel, message: str) -> Coroutine[Any, Any, None]:
  return channel.send(message)


def edit_channel_message(channel: discord.TextChannel, message: str, id: int) -> Coroutine[Any, Any, None]:
  return channel.edit_message(message, id)


def send_channel_file(channel: discord.TextChannel, file: discord.File) -> Coroutine[Any, Any, None]:
  return channel.send(file=file)
