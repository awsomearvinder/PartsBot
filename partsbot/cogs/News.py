import discord
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands, tasks
import asyncio



class News(commands.Cog):

    class MyCog(commands.Cog):
        def __init__(self):
            self.index = 0
            self.printer.start()

        def cog_unload(self):
            self.printer.cancel()

        @tasks.loop(seconds=5.0)
        async def printer(self):
            print(self.index)
            self.index += 1

def setup(bot):
    bot.add_cog(News(bot))