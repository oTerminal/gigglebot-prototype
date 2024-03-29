from asyncio import sleep
from datetime import datetime
from glob import glob
from pathlib import Path
import traceback

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed
from discord import Intents
from discord.ext import commands
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown
from discord.ext.commands import when_mentioned_or

from ..db import db

# PREFIX = "g!"
OWNER_IDS = [485255323502772255]
COGS = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument, MissingRequiredArgument)


def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

   
class Bot(BotBase):
    def __init__(self):
#        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = self.get_guild
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS, intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

        print("Setup complete.")

    def run(self, version):
        self.VERSION = version

        print("Running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

#    async def process_commands(self, message):
#      ctx = await self.get_context(message, cls=Context)
#      if ctx.command is not None and ctx.guild is not None:
#           if self.ready:
#              await self.invoke(ctx)
#
#        else:
#           await ctx.send("I'm not ready to take commands yet, Please try again in a few seconds.")

    async def rules_reminder(self):
        await self.stdout.send("I am a timed notification!")


    async def on_connect(self):
        print("Bot connected!")

    async def on_disconnect(self):
        print("Bot disconnected!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")
        await self.stdout.send("An error occurred")
        raise
    
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        if isinstance(exc, CommandNotFound):
            pass

        elif isinstance(exc, BadArgument):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("1 or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on cooldown, try again in {exc.retry_after:,.2f} seconds.")

        # elif isinstance(exc.original, HTTPException):
        #     await ctx.send("Unable to send the message.")

        elif isinstance(exc.original, Forbidden):
            await ctx.send("I do not have permissions to do that. ")

        elif hasattr(exc, "original"):
            raise exc.original
        
        else:
            raise exc.original


    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(744999017812983910)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()
            self.stdout = self.get_channel(783451644217786409)

            await self.stdout.send("Better bot is now online lmfao ( ͡° ͜ʖ ͡°)")

            embed = Embed(title="Now online!", description="Better bot is online lmfao ( ͡° ͜ʖ ͡°)", color=0x00FFFF, 
                          timestamp=datetime.utcnow())
            fields = [("Help command", "g!help", True),
                     ("Another field", "This field is next to the another one", True),
                     ("A non-inline field", "This field will appear on it's own row", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="CrazyVibes07", icon_url=self.guild.icon_url)
            embed.set_footer(text="haha 69 is funny number lol")
            embed.set_thumbnail(url=self.guild.icon_url)
            await self.stdout.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            print("Bot ready!") 

        else:
            print("Bot reconnected!")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()
