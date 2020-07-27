import random
import discord
import os
from discord.ext import commands


class Imgspam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/cats"))
        await ctx.send(file=discord.File("cats/" + rand))

    @commands.command()
    async def think(self, ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/think"))
        await ctx.send(file=discord.File("think/" + rand))


    @commands.command()
    async def smug(self, ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/smug"))
        await ctx.send(file=discord.File("smug/" + rand))


    @commands.command()
    async def dance(self, ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/dance"))
        try:
            await ctx.send(file=discord.File("dance/" + rand))
        except Exception:
            await ctx.send('command aint workin boss')
            return

    @commands.command()
    async def scatter(self, ctx):
        await ctx.send(file=discord.File("/root/TomodachAI/SCATTER.mp4"))


def setup(bot):
    bot.add_cog(Imgspam(bot))
