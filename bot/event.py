from discord import VoiceState, Member
from enum import Enum


class ToggleState(Enum):
    ON = "on"
    OFF = "off"


class VoiceStateEvent:
    member: Member
    changed_attribute: str
    new_state: ToggleState

    def __init__(self, member: Member, before: VoiceState, after: VoiceState):
        # Please don't judge me
        diff = next(attr for attr in VoiceState.__slots__
                    if before.__getattribute__(attr) != after.__getattribute__(attr))
        self.member = member
        self.changed_attribute = diff
        self.new_value = ToggleState.ON if after.__getattribute__(diff) else ToggleState.OFF


# class InvocationEventType(Enum):
#
#
# class BotInvocationEvent:
#     member: Member
#
#     def __init__(self, member: Member):
#         self.member = member
