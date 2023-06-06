import hashlib

__all__ = ['Snowflake']


class Snowflake:
  """
  Very very big integer
  """

  def __init__(self, value: int | str):
    """
    New Snowflake
    
    ## Parameters
    ```py
    >>> value : int | str
    ```
    initializes the snowflake with the given value
    """
    self.__value: bytes = None
    if isinstance(value, int):
      self.__value = value.to_bytes(8, 'big')
    elif isinstance(value, str):
      self.__value = bytes.fromhex(value)

  def __str__(self):
    return self.__value.hex()

  def __repr__(self):
    return f'Snowflake({self.__value.hex()})'

  def __hash__(self) -> int:
    return int.from_bytes(hashlib.sha512(self.__value).digest(), 'big')

  def __eq__(self, other: 'Snowflake') -> bool:
    return self.__value == other.__value

  def __ne__(self, other: 'Snowflake') -> bool:
    return self.__value != other.__value

  # def __lt__(self, other: 'Snowflake') -> bool:
  #   return self.__value < other.__value

  # def __le__(self, other: 'Snowflake') -> bool:
  #   return self.__value <= other.__value

  # def __gt__(self, other: 'Snowflake') -> bool:
  #   return self.__value > other.__value

  # def __ge__(self, other: 'Snowflake') -> bool:
  #   return self.__value >= other.__value
