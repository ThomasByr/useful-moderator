from dataclasses import dataclass
from discord import Message

import math

from .auto_response_data import *
from ..helper import *

__all__ = ['User', 'Guild', 'Tier']


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
  id: int
  xp: int = 0

  def __post_init__(self):
    self.xp = int(self.xp)

  def xp2lvl(self) -> int:
    return int((self.xp / 100)**0.5)

  def lvl2xp(self) -> int:
    return int((self.xp**2) * 100)

  def xp_from_msg_len(self, msg_len: int) -> int:
    return int(2 * math.log10(msg_len)) + 5

  def additional_xp_per_attachment(self, n_attachments: int) -> int:
    return int(n_attachments + 1)

  def process_message(self, msg: Message) -> int:
    xp = self.xp_from_msg_len(len(msg.content))
    xp += self.additional_xp_per_attachment(len(msg.attachments))
    return self.add_xp(xp)

  def add_xp(self, xp: int) -> int:
    self.xp += xp
    return self.xp


@dataclass
class Guild:
  id: int
  tier: Tier = Tier.T1

  auto_responses: list[AutoResponseData] = None

  def __post_init__(self):
    if self.auto_responses is None:
      self.auto_responses = []

  def to_dict(self) -> dict:
    return {
      'id': self.id,
      'tier': self.tier.value,
      'auto_responses': [d.to_dict() for d in self.auto_responses],
    }

  @classmethod
  def from_dict(cls, d: dict) -> 'Guild':
    return cls(
      id=d['id'],
      tier=Tier(d['tier']),
      auto_responses=[AutoResponseData.from_dict(ad) for ad in d['auto_responses']],
    )

  @staticmethod
  def new(id: int) -> 'Guild':
    return Guild(id=id)
