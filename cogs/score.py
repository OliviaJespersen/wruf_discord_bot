import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

from utils import database, layout


load_dotenv(override=True)

class Score(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    score = discord.SlashCommandGroup("score", "Score commands")

    @discord.user_command(guild_ids=os.getenv("GUILD_IDS").split(","))
    async def show_score(self, ctx: discord.ApplicationContext, member: discord.Member):
        """ Show the W.R.U.F score of a member. """
        score = await database.get_average_score(member.id)
        await ctx.respond(layout.score(member.display_name, score))   

    @score.command()
    async def show_leaderboard(self, ctx: discord.ApplicationContext):
        """ Show the W.R.U.F leaderboard. """
        guild = ctx.guild
        
        scores = await database.get_all_average_scores()
        named_scores = [((await guild.fetch_member(user_id)).display_name, score) for user_id, score in scores]

        await ctx.respond(layout.leaderboard(named_scores))

def setup(bot):
    bot.add_cog(Score(bot))