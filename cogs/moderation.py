from discord.ext import commands
import discord
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello to the bot!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello there!")

    @app_commands.command(name="ban", description="Ban a user from the server")
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ You do not have permission to ban members.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        try:
            await interaction.guild.ban(user, reason=reason)
            await interaction.followup.send(f"✅ {user.name} has been banned.")
        except Exception as e:
            await interaction.followup.send(f"⚠️ Failed to ban user: `{e}`")

    @app_commands.command(name="kick", description="Kick a user from the server")
    async def kick(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("❌ You do not have permission to kick members.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        try:
            await interaction.guild.kick(user, reason=reason)
            await interaction.followup.send(f"✅ {user.name} has been kicked.")
        except Exception as e:
            await interaction.followup.send(f"⚠️ Failed to kick user: `{e}`")

    @app_commands.command(name="timeout", description="Put a user in timeout")
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, duration: int):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ You do not have permission to timeout members.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        try:
            await user.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration))
            await interaction.followup.send(f"✅ {user.name} has been timed out for {duration} seconds.")
        except Exception as e:
            await interaction.followup.send(f"⚠️ Failed to timeout user: `{e}`")

    @app_commands.command(name="purge", description="Delete a number of messages from the channel")
    async def purge(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ You do not have permission to purge messages.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        try:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"🧹 Deleted {len(deleted)} messages.")
        except Exception as e:
            await interaction.followup.send(f"⚠️ Failed to purge messages: `{e}`")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
