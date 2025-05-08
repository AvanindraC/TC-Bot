import discord
from discord.ext import commands
from discord import app_commands
import random
import wikipedia
import pyjokes
from googlesearch import search
from tawpy import Tenor
from bs4 import BeautifulSoup
import requests


def surprise():
    vids = [ 'https://user-images.githubusercontent.com/77975448/130755920-2eeef248-8976-4de1-97db-0421b9631bd1.mp4', 'https://user-images.githubusercontent.com/77975448/130755923-d55eac65-d407-4711-8720-f57fd7389e8c.mp4', 'https://user-images.githubusercontent.com/77975448/130756539-4edb3240-0894-45ad-93b2-2f9c57c6b6ff.mp4',
'https://user-images.githubusercontent.com/77975448/130756569-064040f7-17f9-4923-904e-5fc4ee0fd1da.mp4', 'https://user-images.githubusercontent.com/77975448/130760005-b69b2ba2-8294-4d4c-9976-d5eb379ef2df.mp4', 'https://user-images.githubusercontent.com/77975448/130760014-fc1395af-5b0a-4f63-a2cb-84e92d757ab9.mp4', 'https://user-images.githubusercontent.com/77975448/130760022-9346ee5e-6dcb-402c-a56a-e7bb58db9aaf.mp4', 'https://user-images.githubusercontent.com/77975448/130760038-35a6c47f-dd2b-45a5-900d-866178052345.mp4', 'https://user-images.githubusercontent.com/77975448/130760058-063ad085-4c72-4882-8298-f1d2c332581d.mp4', 'https://user-images.githubusercontent.com/77975448/130760072-a094d2f7-35f6-4716-a638-f63f6d5d2289.mp4',
'https://user-images.githubusercontent.com/77975448/130773300-47e0ee11-de3f-4ae7-b209-4eae9d74e19d.mp4', 'https://user-images.githubusercontent.com/77975448/130773303-88765288-4da4-4f67-bad6-afdc6d5135cf.mp4', 
'https://user-images.githubusercontent.com/77975448/130776465-5d766839-2824-4434-ad57-60384dfc9ae0.mp4', 'https://user-images.githubusercontent.com/77975448/130776602-5279e8a5-3ec5-4857-9d07-1bef7249cb14.mp4', 'https://user-images.githubusercontent.com/77975448/130776588-0b8ab582-fabc-48d5-b98a-0f614315bd5e.mp4', 'https://user-images.githubusercontent.com/77975448/130777016-315d09ad-5677-4b4f-a839-8d33ea27e5a9.mp4', 'https://user-images.githubusercontent.com/77975448/130961886-369efc51-7db0-45a1-87b6-5890d7a7530a.mp4','https://user-images.githubusercontent.com/77975448/130755914-6ef3fb40-0c6c-4c41-a16a-659962a35751.mp4','https://user-images.githubusercontent.com/77975448/130760058-063ad085-4c72-4882-8298-f1d2c332581d.mp4', 'https://user-images.githubusercontent.com/77975448/130963376-0bc1f40a-5bcd-459e-a3cd-5d0adc55ae8d.mp4', 'https://user-images.githubusercontent.com/77975448/130963387-926845d7-76a9-4ed7-8ed8-a9b5360788e7.mp4', 'https://user-images.githubusercontent.com/77975448/130963394-930cbe7a-757c-4156-b7b0-b498bb0bd580.mp4']
    return random.choice(vids)

def get_gif(content):
    tenor = Tenor()
    urls = tenor.search_for_gifs(query=content)
    return random.choice(urls)

def get_joke():
    return pyjokes.get_joke(language='en', category='neutral')


def google_results(query):
    results = list(search(query, num_results=5))
    result_text = ""

    for url in results:
        try:
            response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No Title"
        except Exception as e:
            title = "Failed to fetch title"
        
        result_text += f"[{title}]({url})\n"

    embed = discord.Embed(
        title=f"Top Google results for: {query}",
        description=result_text or "No results found.",
        color=0x00ff99
    )
    return embed

def wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=5)
        embed = discord.Embed(title=f"Wikipedia: {query}", description=summary, color=0xffcc00)
        return embed
    except Exception as e:
        return discord.Embed(title="Error", description=f"Could not fetch Wikipedia article.\n{e}", color=0xff0000)

class Fun(commands.Cog):
    """Fun commands for entertainment."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="joke", description="Tells a random joke")
    async def joke_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(get_joke())

    @app_commands.command(name="surpriseme", description="Fun surprise")
    async def surpriseme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(surprise())

    @app_commands.command(name="google", description="Search Google")
    async def google_cmd(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        embed = google_results(query)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="gif", description="Find a gif on Tenor")
    async def gif_cmd(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        url = get_gif(query)
        embed = discord.Embed(color=discord.Color.teal())
        embed.set_image(url=url)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="wikipedia", description="Search Wikipedia")
    async def wikipedia_cmd(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        embed = wikipedia_summary(query)
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
