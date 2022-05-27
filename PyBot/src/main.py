#IMPORTS
import discord
from discord.ext import commands
import os

# Setting up bot prefix

bot = commands.Bot(command_prefix="!")

for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')




bot.run('OTc5NTIxMjY1MTcxODI4Nzk3.GwfDzK.NoLqcW0FJCStEI7XxlE88AdsYvfZeH0cyM-gEE')   