import os
import json
from discord.ext import commands
from .cog.tts import TTSCog

config_path = os.getenv('ROBOTULI_CONF')
cache_root = os.getenv('ROBOTULI_CACHE')

bot = commands.Bot(commands.when_mentioned_or("!"))
config = json.loads(open(config_path).read())

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    if not os.path.exists(cache_root):
        os.mkdir(cache_root)

bot.add_cog(TTSCog(bot, config['customMessages'], cache_root))
bot.run('NzU3MDQxOTU2NDI0NjQ2NzA3.X2aoQw.FJ4XMvnBd8G1FfjJhdNEpxHuYQ8')
