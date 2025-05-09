from discord.ext import commands
import discord

role_message_id = 1370292122594443344
emoji_to_role = {
    discord.PartialEmoji(name='✅'): 1369364351382982757,  
}

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checked_once = False  

    @commands.Cog.listener()
    async def on_ready(self):
        if self.checked_once:
            return
        self.checked_once = True

        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, id=11369382280283295875)  
            if not channel:
                continue

            try:
                message = await channel.fetch_message(role_message_id)
            except discord.NotFound:
                continue

            for reaction in message.reactions:
                if reaction.emoji in emoji_to_role:
                    role = guild.get_role(emoji_to_role[reaction.emoji])
                    users = await reaction.users().flatten()
                    for user in users:
                        if user.bot:
                            continue
                        member = guild.get_member(user.id) or await guild.fetch_member(user.id)
                        if role and role not in member.roles:
                            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != role_message_id:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        role_id = emoji_to_role.get(payload.emoji)
        if not role_id:
            return
        role = guild.get_role(role_id)
        if not role:
            return
        member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
        if member:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != role_message_id:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        role_id = emoji_to_role.get(payload.emoji)
        if not role_id:
            return
        role = guild.get_role(role_id)
        if not role:
            return
        member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
        if member:
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(RoleManager(bot))
