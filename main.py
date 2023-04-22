import nextcord
from nextcord.ext import commands
import aiohttp
import asyncio
import json
import os
import misc



url = "https://api.warframestat.us/pc/?language=ru"


bot = commands.Bot(command_prefix = ".", intents = nextcord.Intents.all())


@bot.command()
@commands.is_owner()
async def load(ctx, extension: str):
	bot.load_extension(f"cogs.{extension}")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension: str):
	bot.unload_extension(f"cogs.{extension}")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str):
	bot.reload_extension(f"cogs.{extension}")


for filename in os.listdir("cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")


bot.run("MTA5OTAwMjI5MzkwODY3Njc0OA.G7fpbR.IvnpLI5268IhWTngsSDpW916orc8AL6z_j-YsQ")