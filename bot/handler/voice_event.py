from discord import VoiceState, Member
from .. import event


class EventMessageResolver:
    def __init__(self, custom_messages):
        self.custom_messages = custom_messages

    def get_state_message(self, member: Member, before: VoiceState, after: VoiceState):
        state_event = event.VoiceStateEvent(member, before, after)
        return self.custom_messages.get_event_reaction(state_event)
