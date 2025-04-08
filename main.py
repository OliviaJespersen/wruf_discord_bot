import discord
import os
from dotenv import load_dotenv

from exceptions import UserInputError
from utils import system, layout, image


system.log(2, "Starting bot")

load_dotenv(override=True)

intents = discord.Intents.default()
#intents.members = True
#intents.message_content = True
#intents.presences = True

bot = discord.Bot(intents=intents)

for file in os.listdir("./cogs"):
    name, ext = os.path.splitext(file) 
    if ext == ".py":
        bot.load_extension(f"cogs.{name}")

system.log_all_utils()

@bot.event
async def on_ready():
    image.create_session()
    
    system.log(0, f"{bot.user} is running")

@bot.event
async def on_application_command(ctx: discord.ApplicationContext):
    system.log(2, f"{ctx.user} used command: {ctx.command.qualified_name}")

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.ApplicationCommandInvokeError):
    original = error.original
    if isinstance(original, UserInputError):
        await ctx.respond(layout.error("Invalid input", original))
        system.log(1, f"User input error: {original}")
    else:
        await ctx.respond(layout.error("There was an unexpected error"))
        system.log(3, f"Unexpected error: {original}")

    system.reset_dynamic_indent()

@bot.event
async def on_application_command_completion(ctx: discord.ApplicationContext):
    system.log(0, f"{ctx.user} completed command: {ctx.command.qualified_name}")

bot.run(os.getenv("BOT_TOKEN"))
