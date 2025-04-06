import os
import sys
import discord
from discord.ext import commands

from utils import database, image


class Admin(commands.Cog):
    """ Admin commands for bot management. """
    def __init__(self, bot):
        self.bot = bot

    admin = discord.SlashCommandGroup("admin", "Admin commands")

    @admin.command()
    @commands.is_owner()
    async def shut_down(self, ctx: discord.ApplicationContext):
        """ Shuts down the bot. """
        await ctx.respond("Shutting down")
        await image.close_session()
        await self.bot.close()

    @admin.command()
    @commands.is_owner()
    async def restart(self, ctx: discord.ApplicationContext):
        """ Restarts the bot. """
        await ctx.respond(f"Restarting bot")
        os.execv(sys.executable, ['python'] + sys.argv)

    @admin.command()
    @commands.is_owner()
    async def clear_scores(self, ctx: discord.ApplicationContext):
        """ Clears all user scores. """
        await database.clear_scores()
        await ctx.respond("Scores cleared")

    @admin.command()
    @commands.is_owner()
    async def clear_resources(self, ctx: discord.ApplicationContext):
        """ Clears all used resources. """
        await database.clear_resources()
        await ctx.respond("Resources cleared")

    @admin.command()
    @commands.is_owner()
    async def clear_database(self, ctx: discord.ApplicationContext):
        """ Clears the database. """
        await database.clear_database()
        await ctx.respond("Database cleared")
        
def setup(bot):
    bot.add_cog(Admin(bot))