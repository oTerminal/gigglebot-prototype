from discord.ext import commands
from discord.ext.commands import Cog, has_permissions, command, CheckFailure
import discord
import os
import traceback
import asyncio
from datetime import datetime

from ..db import db

# Ping command for the bot.

class Config(Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
  		await ctx.send(f'Pong! {round(self.bot.latency *1000)}ms')

	@commands.command(name='reload', description="Reload all or 1 cog.")
	@commands.is_owner()
	async def reload(self, ctx, cog=None):
		if not cog:
			async with ctx.typing():
				embed = discord.Embed(
					title="Reloading all cogs!",
					color=0x808080,
					timestamp=ctx.message.created_at
				)
				for ext in os.listdir("./lib/cogs/"):
					if ext.endswith(".py") and not ext.startswith("_"):
						try:
							self.bot.reload_extension(f"lib.cogs.{ext[:-3]}")
							embed.add_field(
								name=f"Reloaded: `{ext}`",
								value='\uFEFF',
								inline=False
							)
						except Exception as e:
							embed.add_field(
								name=f"Failed to reload: `{ext}`",
								value=e,
								inline=False
							)
						await asyncio.sleep(0.5)
				await ctx.send(embed=embed)
		else:
			async with ctx.typing():
				embed = discord.Embed(
					title="Reloading cog!",
					color=0x808080,
					timestamp=ctx.message.created_at
				)
				ext = f"{cog.lower()}.py"
				if not os.path.exists(f"./lib/cogs/{ext}"):
					embed.add_field(
						name=f"Failed to reload: `{ext}`",
						value="This cog does not exist.",
						inline=False
					)

				elif ext.endswith(".py") and not ext.startswith("_"):
					try:
						self.bot.reload_extension(f"lib.cogs.{ext[:-3]}")
						embed.add_field(
							name=f"Reloaded: `{ext}`",
							value='\uFEFF',
							inline=False
						)
					except Exception:
						desired_trace = traceback.format_exc()
						embed.add_field(
							name=f"Failed to reload: `{ext}`",
							value=desired_trace,
							inline=False
						)
				await ctx.send(embed=embed)

	@commands.command(name='load', description="Load 1 or all cogs")
	@commands.is_owner()
	async def load(self, ctx, cog=None):
		if not cog:
			async with ctx.typing():
				embed = discord.Embed(
					title="Loading all cogs!",
					color=0x808080,
					timestamp=ctx.message.created_at
				)
				for ext in os.listdir("./lib/cogs/"):
					if ext.endswith(".py") and not ext.startswith("_"):
						try:
							self.bot.load_extension(f"lib.cogs.{ext[:-3]}")
							embed.add_field(
								name=f"Loaded: `{ext}`",
								value='\uFEFF',
								inline=False
							)
						except Exception as e:
							embed.add_field(
								name=f"Failed to Load: `{ext}`",
								value=e,
								inline=False
							)
						await asyncio.sleep(0.5)
				await ctx.send(embed=embed)
		else:
			async with ctx.typing():
				embed = discord.Embed(
					title="Loading all cogs!",
					color=0x808080,
					timestamp=ctx.message.created_at
				)
				ext = f"{cog.lower()}.py"
				if not os.path.exists(f"./lib/cogs/{ext}"):
					embed.add_field(
						name=f"Failed to Load: `{ext}`",
						value="This cog does not exist.",
						inline=False
					)

				elif ext.endswith(".py") and not ext.startswith("_"):
					try:
						self.bot.load_extension(f"lib.cogs.{ext[:-3]}")
						embed.add_field(
							name=f"Loaded: `{ext}`",
							value='\uFEFF',
							inline=False
						)
					except Exception:
						desired_trace = traceback.format_exc()
						embed.add_field(
							name=f"Failed to Load: `{ext}`",
							value=desired_trace,
							inline=False
						)
				await ctx.send(embed=embed)

	@commands.command(name='unload', description="Unload 1 or all cogs.")
	@commands.is_owner()
	async def unload(self, ctx, cog=None):
		if not cog:
			async with ctx.typing():
				embed = discord.Embed(
					title="Unloading all cogs!",
					color=0x808080,
					timestamp=ctx.message.created_at
				)
				for ext in os.listdir("./lib/cogs/"):
					if ext.endswith(".py") and not ext.startswith("_"):
						try:
							self.bot.unload_extension(f"lib.cogs.{ext[:-3]}")
							embed.add_field(
								name=f"Unloaded: `{ext}`",
								value='\uFEFF',
								inline=False
							)
						except Exception as e:
							embed.add_field(
								name=f"Failed to unload: `{ext}`",
								value=e,
								inline=False
							)
						await asyncio.sleep(0.5)
				await ctx.send(embed=embed)
		else:
			async with ctx.typing():
				embed = discord.Embed(
					title="Unload all cogs!",
					color=0x808080,
					timestamp=ctx.message.created_at
				)
				ext = f"{cog.lower()}.py"
				if not os.path.exists(f"./lib/cogs/{ext}"):
					embed.add_field(
						name=f"Failed to unload: `{ext}`",
						value="This cog does not exist.",
						inline=False
					)

				elif ext.endswith(".py") and not ext.startswith("_"):
					try:
						self.bot.unload_extension(f"lib.cogs.{ext[:-3]}")
						embed.add_field(
							name=f"Unloaded: `{ext}`",
							value='\uFEFF',
							inline=False
						)
					except Exception:
						desired_trace = traceback.format_exc()
						embed.add_field(
							name=f"Failed to unload: `{ext}`",
							value=desired_trace,
							inline=False
						)
				await ctx.send(embed=embed)

	@commands.command(name="info", description="Display's info about the bot!")
	async def info(self, ctx):
		embed = discord.Embed(title="Bot info!",
							  description="Some info about the bot is present here :D",
							  color=ctx.author.color,
							  timestamp=datetime.utcnow())
		embed.add_field(name="Owner", value="`CrazyVibes07#3156`" + "\n" "`ID=485255323502772255`", inline=True)
		embed.add_field(name="Python version", value="`3.8.5`")
		embed.add_field(name="Discord.py version", value="`1.6.0`")
		embed.set_footer(text=ctx.message.author, icon_url=ctx.guild.icon_url)
		await ctx.send(embed=embed)

	@command(name="prefix")
	@has_permissions(manage_guild=True)
	async def change_prefix(self, ctx, new: str):
		if len(new) > 5:
			await ctx.send("The prefix can not be longer than 5 characters in length. ")

		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
			await ctx.send(f"Prefix set to {new}")

def setup(bot):
	bot.add_cog(Config(bot))