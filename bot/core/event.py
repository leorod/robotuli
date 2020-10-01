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


class InvocationType(Enum):
    JOIN = "join"
    ALREADY_JOINED = "already_joined"
    MEMBER_NOT_JOINED = "member_not_joined"


class BotInvocationEvent:
    member: Member
    invocation_type: InvocationType

    def __init__(self, member: Member, invocation_type: InvocationType):
        self.member = member
        self.invocation_type = invocation_type
