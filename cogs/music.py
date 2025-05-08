import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import requests
import re

def geturl(song_name: str) -> str:
    query = "+".join(song_name.split())
    url = f"https://www.youtube.com/results?search_query={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
    return f"https://www.youtube.com/watch?v={video_ids[0]}" if video_ids else None

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play", description="Play a song from YouTube")
    async def play(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer(thinking=True)

        if not interaction.user.voice:
            await interaction.followup.send("You must be in a voice channel.")
            return

        voice_channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client

        if vc is None:
            vc = await voice_channel.connect()
        elif vc.channel != voice_channel:
            await vc.move_to(voice_channel)

        # If user entered a search query
        if not query.startswith("http"):
            query = geturl(query)
            if not query:
                await interaction.followup.send("Could not find the song.")
                return

        ytdl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
        }

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        try:
            with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                audio_url = info['url']
                title = info.get('title', 'Unknown')

            vc.stop()
            source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
            vc.play(source, after=lambda e: print(f"Finished playing: {e}" if e else "Finished playing."))

            await interaction.followup.send(f"🎵 Now playing: **{title}**")

        except Exception as e:
            await interaction.followup.send(f"Error: `{e}`")

    @app_commands.command(name="join", description="Join your voice channel")
    async def join(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.followup.send(f"Joined {channel.name}!")
        else:
            await interaction.followup.send("You need to be in a voice channel.")

    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            await interaction.followup.send("Left the voice channel.")
        else:
            await interaction.followup.send("I'm not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))
