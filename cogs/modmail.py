import discord
from discord.ext import commands
from discord import app_commands

MOD_ROLE_ID = 1370086445745831956
MODMAIL_CHANNEL_ID = 1370260029818540052 

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(MODMAIL_CHANNEL_ID)
        if channel:
            try:
                await channel.purge(limit=None)
            except Exception as e:
                print(f"Failed to purge modmail channel: {e}")
            await channel.send(
                embed=discord.Embed(
                    title="ModMail",
                    description="Click the button below to start a private thread with the moderators.",
                    color=discord.Color.green()
                ),
                view=ModMailButtonView(self.bot)
            )

class ModMailButtonView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="ModMail", style=discord.ButtonStyle.blurple)
    async def modmail_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user
        channel = interaction.channel

        thread = await channel.create_thread(
            name=f"ModMail - {member.display_name}",
            type=discord.ChannelType.private_thread,
            invitable=False
        )
        await thread.add_user(member)

        mod_role = guild.get_role(MOD_ROLE_ID)
        if mod_role:
            for mod in mod_role.members:
                try:
                    await thread.add_user(mod)
                except:
                    pass

        await thread.send(f"Hello {member.mention}, a moderator will be with you shortly.")
        await interaction.response.send_message("A modmail thread has been created!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModMail(bot))
