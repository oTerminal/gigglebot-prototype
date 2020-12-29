from discord.ext import commands

from discord.ext.commands import Cog


# Ping command for the bot.

class Ping(Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
  		await ctx.send(f'Pong! {round(self.bot.latency *1000)}ms')

def setup(bot):
	bot.add_cog(Ping(bot))