import time
from discord.ext import commands
from ..handler.tts import TTS
from ..handler.CustomMessages import CustomMessages


class TTSCog(commands.Cog):
    def __init__(self, bot, custom_messages, cache_root=None):
        self.bot = bot
        self.tts = TTS(cache_root)
        self.custom_messages = CustomMessages(custom_messages)

    async def join_voice(self, ctx):
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member != self.bot.user:
            if after.channel is not None:
                for client in filter(lambda c: c.channel == after.channel, self.bot.voice_clients):
                    time.sleep(0.5)  # Wait 500 millis for the user to finish connecting
                    self.tts.say(self.custom_messages.get_welcome(member.display_name), client)
            else:
                for client in filter(lambda c: c.channel == before.channel, self.bot.voice_clients):
                    self.tts.say(self.custom_messages.get_goodbye(member.display_name), client)

    @commands.command()
    async def say(self, ctx, *, text=None):
        await self.join_voice(ctx)
        self.tts.say(text, ctx.voice_client)

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""
        if ctx.author.voice is None:
            await ctx.send(self.custom_messages.get_user_not_joined())
            return
        if ctx.voice_client:
            self.tts.say(self.custom_messages.get_already_joined(), ctx.voice_client)
        else:
            await self.join_voice(ctx)
            self.tts.say(self.custom_messages.get_entrance(), ctx.voice_client)
