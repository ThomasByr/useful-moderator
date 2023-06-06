import os

from src import UsefulClient

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
BOT_INVITE = os.getenv('BOT_INVITE')

if __name__ == '__main__':

  client = UsefulClient(BOT_PREFIX, BOT_INVITE, help_command=None)
  client.run(BOT_TOKEN)
