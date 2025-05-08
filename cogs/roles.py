from discord.ext import commands
import discord


role_message_id = 1369628936648265799
emoji_to_role = {
    discord.PartialEmoji(name='👍'): 1369364351382982757,
}

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

