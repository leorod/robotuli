import random
from . import event
from discord import VoiceState, Member


def _random_message(collection, member_name=None):
    template = random.choice(collection)
    return template.replace('${member}', member_name)


class MessageBuilder:
    def __init__(self, templates):
        self.templates = templates

    def prebake(self, member_names):
        templates = []
        messages = []
        for template_group in self.templates.values():
            templates.extend(template_group)
        for member in member_names:
            messages.extend([msg.replace('${member}', member) for msg in templates])
        return messages

    def get_event_reaction(self, event: event.VoiceStateEvent):
        reaction_templates = self.templates[event.changed_attribute][event.new_value.value]
        return _random_message(reaction_templates, event.member.display_name)

    def get_command_response(self, event: event.BotInvocationEvent):
        return _random_message(self.templates[event.invocation_type.value], event.member.display_name)


class EventMessageResolver:
    def __init__(self, custom_messages):
        self.custom_messages = custom_messages

    def get_state_message(self, member: Member, before: VoiceState, after: VoiceState):
        state_event = event.VoiceStateEvent(member, before, after)
        return self.custom_messages.get_event_reaction(state_event)