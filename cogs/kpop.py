import random
import discord
import os
from discord.ext import commands


class Kpop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jimin(self, ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/jimin"))
        await ctx.send(file=discord.File("jimin/" + rand))

    @commands.command()
    async def suga(self, ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/suga"))
        await ctx.send(file=discord.File("suga/" + rand))

    @commands.command()
    async def V(self, ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/V"))
        await ctx.send(file=discord.File("V/" + rand))

    @commands.command()
    async def jin(self, ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/jin"))
        await ctx.send(file=discord.File("jin/" + rand))


def setup(bot):
    bot.add_cog(Kpop(bot))
