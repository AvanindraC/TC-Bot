from discord.ext import commands
import discord

class ServerEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = member.guild.get_channel(1369382044119076895)
        if welcome_channel:
            await welcome_channel.send(f"Welcome {member.mention} to {member.guild.name}!")

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)
        
        if message.content.strip() == f"<@{self.bot.user.id}>":
            embed = discord.Embed(
                title="👋 Hello! I'm TC-Bot",
                description="I'm here to help moderate your server and manage roles.\n\nHere are some commands you can try:",
                color=discord.Color.blue()
            )
            embed.add_field(name="/hello", value="Say hi to the bot!", inline=False)
            embed.add_field(name="/kick", value="Kick a member (if you have permissions)", inline=False)
            embed.add_field(name="/ban", value="Ban a member (if you have permissions)", inline=False)
            embed.add_field(name="/timeout", value="Timeout a member temporarily", inline=False)
            embed.add_field(name="/purge", value="Delete recent messages", inline=False)
            await message.channel.send(embed=embed)

                
        
        if message.channel.id != 1369383542404022272:
            return

        role = message.guild.get_role(1369364351382982757)
        if not role:
            return
        for member in role.members:
            try:
                await member.send(f"New message in #{message.channel.name} from {message.author.display_name}:{message.content}")
            except discord.Forbidden:
                pass

async def setup(bot):
    await bot.add_cog(ServerEvents(bot))
