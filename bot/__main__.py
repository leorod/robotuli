import os
import json
from discord.ext import commands
from bot.tts.cog import TTSCog

config_path = os.getenv('ROBOTULI_CONF')
cache_root = os.getenv('ROBOTULI_CACHE')
bot_token = os.getenv('ROBOTULI_TOKEN')

bot = commands.Bot(commands.when_mentioned_or("!"))
config = json.loads(open(config_path).read())

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    if not os.path.exists(cache_root):
        os.mkdir(cache_root)

bot.add_cog(TTSCog(bot, config['event_templates'], cache_root))
bot.run(bot_token)
