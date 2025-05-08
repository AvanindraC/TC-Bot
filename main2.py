import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

synced = False

@bot.event
async def on_ready():
    global synced
    if not synced:
        try:
            await tree.sync()
            print("Slash commands synced.")
            synced = True
        except Exception as e:
            print(f"Failed to sync commands: {e}")
    print(f"Logged in as {bot.user} ({bot.user.id})")

initial_extensions = [
    "cogs.moderation",
    "cogs.roles",
    "cogs.events",
    #"cogs.music",
    "cogs.misc"
]

async def main():
    async with bot:
        for ext in initial_extensions:
            try:
                await bot.load_extension(ext)
                print(f"Loaded extension: {ext}")
            except Exception as e:
                print(f"Failed to load {ext}: {e}")
        await bot.start(TOKEN)

asyncio.run(main())