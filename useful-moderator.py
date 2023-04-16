import os

from src import UsefulClient, UsefulFormatter, console_handler, log_lvl


def get_token() -> str:
  return os.getenv('BOT_TOKEN')
def get_prefix() -> str:
  return os.getenv('BOT_PREFIX', '!')


BOT_TOKEN = get_token()
BOT_PREFIX = get_prefix()

if __name__ == '__main__':

  client = UsefulClient(BOT_PREFIX, help_command=None)
  client.run(
    BOT_TOKEN,
    reconnect=True,
    log_handler=console_handler,
    log_formatter=UsefulFormatter(),
    log_level=log_lvl,
  )
