from dataclasses import dataclass

from ..helper.auto_numbered import AutoNumberedEnum


@dataclass
class ExportUserEntry:

  id: int
  xp: int


@dataclass
class ReactionRolesData:
  # https://github.com/Rapptz/discord.py/blob/master/examples/views/persistent.py

  @dataclass
  class ButtonData:
    button_custom_id: str
    role_ids: list[int]
    emote: str
    text: str

  @dataclass
  class RoleGroup:
    role_ids: list[int]
    multiple_allowed: bool

  @dataclass
  class RoleMap:
    role_id: int
    next_allowed_role_ids: list[int]

  msg_id: int
  view_content: list[ButtonData]
  role_groups: list[RoleGroup]
  role_maps: list[RoleMap]


class GuildLvl(AutoNumberedEnum):

  T0 = () # pretty much useless
  T1 = () # base level
  T2 = () # async commands
  T3 = () # real time commands
  T4 = () # admin level
  T5 = () # root level


@dataclass
class ExportGuildEntry:

  id: int
  perms_lvl: GuildLvl
  rr: list[ReactionRolesData]
