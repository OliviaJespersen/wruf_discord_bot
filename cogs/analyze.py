import discord
from discord.ext import commands

from utils import analyzer


class Analyze(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    analyze = discord.SlashCommandGroup("analyze", "Analyze commands")
    
    @analyze.command()
    @discord.option(
        name="image_to_analyze", 
        parameter_name="image",
        description="The image you want to analyze",
    )
    @discord.option(
        name="deep_analysis", 
        parameter_name="deep",
        description="Include a deeper description of the image",
        default=False,
    )
    async def image(self, ctx: discord.ApplicationContext, image: discord.Attachment, deep: bool):
        """ Analyze an image. """
        await ctx.respond("🔄 Processing...")
        messages = await analyzer.image_analysis(image.url, ctx.author.display_name, ctx.author.id, deep=deep)

        for message in messages:
            await ctx.send(message)

def setup(bot):
    bot.add_cog(Analyze(bot))