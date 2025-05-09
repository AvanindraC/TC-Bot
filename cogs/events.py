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


        try:
            embed = discord.Embed(
                title="👋 Welcome to the Server!",
                description=(
                    f"Hey {member.display_name}, welcome to **{member.guild.name}**! 🎉\n\n"
                "We're glad to have you here. Feel free to explore the channels, ask questions, "
                "and get involved in the community!\n\n"
                "If you need help, just mention a moderator or use `/help` to see available commands."
                ),
                color=discord.Color.green()
        )
            embed.set_footer(text="Enjoy your stay!")
            await member.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)
        
        if message.content.strip() == f"<@{self.bot.user.id}>":
            embed = discord.Embed(
            title="👋 Hello! I'm TC-Bot",
            description="Here are my available commands:",
            color=discord.Color.blue()
        )

            commands = await self.bot.tree.fetch_commands()
            for cmd in commands:
                embed.add_field(name=f"/{cmd.name}", value=cmd.description or "No description", inline=False)

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
