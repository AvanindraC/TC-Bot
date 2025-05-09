import discord
from discord.ext import commands
from discord import app_commands

REQUIRED_ROLE_ID = 1370086445745831956

class ServerRules(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="serverrules", description="Send the server rules embed.")
    @app_commands.describe(channel="The channel to send the rules in")
    async def server_rules(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel = None
    ):
        if not isinstance(interaction.user, discord.Member):
            member = await interaction.guild.fetch_member(interaction.user.id)
        else:
            member = interaction.user

        # Optional: restrict who can run this command
        if REQUIRED_ROLE_ID not in [role.id for role in member.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Server Rules",
            color=discord.Color.green()
        )

        embed.add_field(
            name="1. Be respectful",
            value="Be kind and respectful to all members of this server and its partners. Harassment, personal attacks, or insults of any kind will not be tolerated. This extends not only to your fellow members but also to CC members.",
            inline=False,
        )

        embed.add_field(
            name="2. Keep controversial topics to a minimum",
            value="Avoid strong opinions, heated discussions, and sensitive topics like religion and politics to prevent conflict.",
            inline=False,
        )

        embed.add_field(
            name="3. No inappropriate language",
            value="Mild swearing is okay in casual channels only. Let's keep official/help channels safe and welcoming for all.",
            inline=False,
        )

        embed.add_field(
            name="4. Respect personal boundaries",
            value="Don't make others uncomfortable. Respect privacy and personal space. Let everyone feel welcome.",
            inline=False,
        )

        embed.add_field(
            name="5. No NSFW or adult material",
            value="This includes anything pornographic or sexual. Violations result in immediate action.",
            inline=False,
        )

        embed.add_field(
            name="6. Refrain from discrimination",
            value="Sexism, racism, xenophobia, offensive names/profile pics are not allowed. Be respectful to all.",
            inline=False,
        )

        embed.add_field(
            name="7. Follow Discord Guidelines",
            value="[discord.com/guidelines](https://discord.com/guidelines) — applies to everyone on the server.",
            inline=False,
        )

        embed.add_field(
            name="8. No false/misleading info",
            value="Fact-check before sharing. Don't spread misinformation.",
            inline=False,
        )

        embed.add_field(
            name="9. No malware or harmful software",
            value="Keep our server safe. Don't distribute malicious links or programs.",
            inline=False,
        )

        embed.set_footer(text="React to this message to gain server permissions")

        target_channel = channel or interaction.channel
        await target_channel.send(embed=embed)
        await interaction.response.send_message(f"Server rules sent in {target_channel.mention}!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerRules(bot))
