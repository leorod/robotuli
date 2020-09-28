import random


class CustomMessages:
    def __init__(self, templates):
        self.templates = templates

    @staticmethod
    def __random_message(member_name, collection):
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

    def get_welcome(self, member_name):
        return CustomMessages.__random_message(member_name, self.templates['welcome'])

    def get_goodbye(self, member_name):
        return CustomMessages.__random_message(member_name, self.templates['goodbye'])

    def get_entrance(self):
        return random.choice(self.templates['entrances'])

    def get_already_joined(self):
        return random.choice(self.templates['alreadyJoined'])

    def get_user_not_joined(self):
        return random.choice(self.templates['userNotJoined'])
