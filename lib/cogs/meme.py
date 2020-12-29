from discord.ext.commands import command

import random

from discord.ext.commands import Cog

import discord

from aiohttp import request

import aiohttp

class Meme(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="meme")
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://meme-api.herokuapp.com/gimme/memes') as r:
                res = await r.json()
                
            embed = discord.Embed(title=res['title'], url=res['postLink'], color=ctx.author.color)
            embed.set_image(url=res['url'])

            await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Meme(bot))
