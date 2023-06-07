from dataclasses import dataclass

import math

from .auto_response_data import *
from ..helper import *

__all__ = ['User', 'Guild']


class Tier(AutoNumberedEnum):
  T1 = ()
  T2 = ()
  T3 = ()
  T4 = ()
  T5 = ()

  def get_n_auto_responses(self) -> int:
    """
    get the number of maximum auto responses for the tier

    ## Returns
    ```py
    int : n
    ```
    """
    return {
      Tier.T1: 0,
      Tier.T2: 10,
      Tier.T3: 50,
      Tier.T4: 50,
      Tier.T5: 100,
    }[self]


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

  def xp_from_msg_len(self, msg_len: int) -> int:
    return int(2 * math.log10(msg_len)) + 5

  def add_xp(self, xp: int) -> int:
    self.xp += xp
    return self.xp


@dataclass
class Guild:
  id: Snowflake
  tier: Tier = Tier.T1

  auto_responses: list[AutoResponseData] = None
