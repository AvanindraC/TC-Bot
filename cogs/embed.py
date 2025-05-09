import discord
from discord.ext import commands
from discord import app_commands

REQUIRED_ROLE_ID = 1370086445745831956

class EmbedSender(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sendembed", description="Send a custom embed message.")
    @app_commands.describe(
        title="Title of the embed",
        description="Main text of the embed",
        color="Hex color (e.g., #00ff99)",
        channel="The channel to send the embed in"
    )
    async def send_embed(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        color: str = "#00ff99",
        channel: discord.TextChannel = None
    ):
        if not isinstance(interaction.user, discord.Member):
            member = await interaction.guild.fetch_member(interaction.user.id)
        else:
            member = interaction.user

        if REQUIRED_ROLE_ID not in [role.id for role in member.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        try:
            embed = discord.Embed(title=title, description=description, color=int(color.lstrip("#"), 16))
            target_channel = channel or interaction.channel
            await target_channel.send(embed=embed)
            await interaction.response.send_message(f"Embed sent to {target_channel.mention}!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error creating embed: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(EmbedSender(bot))
