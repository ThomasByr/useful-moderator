from typing import NoReturn

from .logger import *


def debug(msg: str, *args, **kwargs) -> None:
  """
  Logs a message with level DEBUG on the root logger.

  ## Parameters
  ```py
  >>> msg : str
  ```
  The message format string. This string may contain {}-style
  """
  logger.debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs) -> None:
  """
  Logs a message with level INFO on the root logger.

  ## Parameters
  ```py
  >>> msg : str
  ```
  The message format string. This string may contain {}-style  
  """
  logger.info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs) -> None:
  """
  Logs a message with level WARNING on the root logger.

  ## Parameters
  ```py
  >>> msg : str
  ```
  The message format string. This string may contain {}-style  
  """
  logger.warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs) -> None:
  """
  Logs a message with level ERROR on the root logger.

  ## Parameters
  ```py
  >>> msg : str
  ```
  The message format string. This string may contain {}-style  
  """
  logger.error(msg, *args, **kwargs)


def critical(msg: str, *args, **kwargs) -> NoReturn:
  """
  Logs a message with level CRITICAL on the root logger
  and then raise an `Exception` with the same arguments.

  ## Parameters
  ```py
  >>> msg : str
  ```
  The message format string. This string may contain {}-style  
  
  ## Returns
  ```py
  NoReturn : None
  ```
  """
  logger.critical(msg, *args, **kwargs)
  # remove exc_info: _ExcInfoType = None,
  #        stack_info: bool = False,
  #        stacklevel: int = 1,
  #        extra: Mapping[str, object] | None = None
  # from the kwargs
  kwargs.pop('exc_info', None)
  kwargs.pop('stack_info', None)
  kwargs.pop('stacklevel', None)
  kwargs.pop('extra', None)
  raise Exception(msg.format(*args, **kwargs))
