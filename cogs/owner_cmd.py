import nextcord
from nextcord.ext import commands, application_checks
import asyncio


class CMDOwners(commands.Cog):

	def __init__(self, bot):
		self.bot = bot





def setup(bot):
	bot.add_cog(CMDOwners(bot))