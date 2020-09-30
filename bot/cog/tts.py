import time
from discord.ext import commands
from ..handler.tts import TTS
from ..handler.CustomMessages import CustomMessages
from ..handler.voice_event import EventMessageResolver

class TTSCog(commands.Cog):
    def __init__(self, bot, custom_messages, cache_root=None):
        self.bot = bot
        self.tts = TTS(cache_root)
        self.custom_messages = CustomMessages(custom_messages)
        self.event_message_resolver = EventMessageResolver(self.custom_messages)

    async def join_voice(self, ctx):
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot:
            channel = after.channel or before.channel
            for voice_client in filter(lambda c: c.channel == channel, self.bot.voice_clients):
                reaction_message = self.event_message_resolver.get_state_message(member, before, after)
                time.sleep(0.5)  # Waiting 500 millis for the member to finish connecting to the voice channel 
                self.tts.say(reaction_message, voice_client)

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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prebake(self, ctx):
        print('Prebaking...')
        messages = self.custom_messages.prebake([m.name for m in ctx.guild.members])
        status = None
        for i in range(0, len(messages)):
            if i == 0:
                status = await ctx.send(f'Prebaking {i + 1}/{len(messages)}')
            else:
                await status.edit(content=f'Prebaking {i + 1}/{len(messages)}')
            self.tts.generate_tts(messages[i])
        print('Prebake complete')
        await status.edit(content='Prebake complete!')
