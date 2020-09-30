import random
from ..event import VoiceStateEvent


class CustomMessages:
    def __init__(self, templates):
        self.templates = templates

    @staticmethod
    def _random_message(member_name, collection):
        template = random.choice(collection)
        return template.replace('${member}', member_name)

    def prebake(self, member_names):
        templates = []
        messages = []
        for template_group in self.templates.values():
            templates.extend(template_group)
        for member in member_names:
            messages.extend([msg.replace('${member}', member) for msg in templates])
        return messages

    def get_event_reaction(self, event: VoiceStateEvent):
        attr_state = "on" if event.new_value else "off"
        reaction_templates = self.templates[event.changed_attribute][event.new_value.value]
        return CustomMessages._random_message(event.member.display_name, reaction_templates)

    def get_entrance(self):
        return random.choice(self.templates['entrances'])

    def get_already_joined(self):
        return random.choice(self.templates['alreadyJoined'])

    def get_user_not_joined(self):
        return random.choice(self.templates['userNotJoined'])
