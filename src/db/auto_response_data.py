from dataclasses import dataclass

from ..helper import *

__all__ = ['AutoResponseData', 'AutoResponsePosition', 'AutoResponseMode']


class AutoResponsePosition(AutoNumberedEnum):
  BEGINNING = ()
  END = ()
  ANYWHERE = ()


class AutoResponseMode(AutoNumberedEnum):
  EXACT = ()
  WITH_CORRECTION = ()


@dataclass
class AutoResponseData:
  id: int
  triggers: set[str]
  position: AutoResponsePosition = AutoResponsePosition.ANYWHERE
  mode: AutoResponseMode = AutoResponseMode.WITH_CORRECTION
  reply: bool = False
  text: str = None
  emote: str = None

  def __post_init__(self):
    self.triggers = set(self.triggers)
    if self.text is not None:
      self.text = str(self.text)
    if self.emote is not None:
      self.emote = str(self.emote)

  def to_dict(self) -> dict:
    return {
      'id': self.id,
      'triggers': list(self.triggers),
      'position': self.position.value,
      'mode': self.mode.value,
      'reply': self.reply,
      'text': self.text,
      'emote': self.emote,
    }

  @classmethod
  def from_dict(cls, d: dict) -> 'AutoResponseData':
    return cls(
      id=d['id'],
      triggers=set(d['triggers']),
      position=AutoResponsePosition(d['position']),
      mode=AutoResponseMode(d['mode']),
      reply=d['reply'],
      text=d['text'],
      emote=d['emote'],
    )
