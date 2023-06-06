import os

from src import UsefulClient


def get_token() -> str:
  return os.getenv('BOT_TOKEN')


def get_prefix() -> str:
  return os.getenv('BOT_PREFIX', '!')


def get_invite() -> str:
  return os.getenv('BOT_INVITE')


BOT_TOKEN = get_token()
BOT_PREFIX = get_prefix()
BOT_INVITE = get_invite()

if __name__ == '__main__':

  client = UsefulClient(BOT_PREFIX, BOT_INVITE, help_command=None)
  client.run(BOT_TOKEN)
