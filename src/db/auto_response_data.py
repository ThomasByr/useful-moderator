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
  id: Snowflake
  triggers: set[str]
  position: AutoResponsePosition = AutoResponsePosition.ANYWHERE
  mode: AutoResponseMode = AutoResponseMode.WITH_CORRECTION
  reply: bool = False
  text: str = None
  emote: str = None
