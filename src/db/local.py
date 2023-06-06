from typing_extensions import override
from dataclasses import dataclass

from ..helper import *

__all__ = ['User', 'Guild']


@dataclass
class User:
  id: Snowflake
  xp: int = 0

  def __post_init__(self):
    self.xp = int(self.xp)

  def xp2lvl(self) -> int:
    return int((self.xp / 100)**0.5)

  def lvl2xp(self) -> int:
    return int((self.xp**2) * 100)


@dataclass
class Guild:
  id: Snowflake
  custom_prefix: str = None
