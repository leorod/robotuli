import os
import discord
import hashlib
from gtts import gTTS

class TTS:
    def __init__(self, cache_root):
        self.cache_path = cache_root + '/tts'
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)

    def generate_tts(self, text):
        filename = hashlib.sha1(bytes(text, 'utf-8')).hexdigest()
        mp3_path = f'{self.cache_path}/{filename}.mp3'
        if not os.path.exists(mp3_path):
            tts = gTTS(text, lang='es')
            tts.save(mp3_path)
        return mp3_path

    def say(self, text, voice_client):
        mp3_path = self.generate_tts(text)
        try:
            voice_client.play(discord.FFmpegPCMAudio(mp3_path), after=lambda e: print(f"Finished playing: {e}"))
        except Exception as e:
            print(e)
