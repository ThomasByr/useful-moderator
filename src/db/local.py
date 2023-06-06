from dataclasses import dataclass

from ..helper import *

__all__ = ['User', 'Guild']


class Tier(AutoNumberedEnum):
  T1 = ()
  T2 = ()
  T3 = ()
  T4 = ()
  T5 = ()


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
  tier: Tier = Tier.T1
