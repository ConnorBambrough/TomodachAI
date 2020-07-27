import random
import discord
import os
from discord.ext import commands


class Kpop():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jimin(ctx):
        rand = random.choice(os.listdir("root\TomodachAI\jimin"))
        await ctx.send(file=discord.File("jimin/" + rand))

    @commands.command()
    async def suga(ctx):
        rand = random.choice(os.listdir("root\TomodachAI\suga"))
        await ctx.send(file=discord.File("suga/" + rand))

    @commands.command()
    async def V(ctx):
        rand = random.choice(os.listdir("/root/TomodachAI/V"))
        await ctx.send(file=discord.File("V/" + rand))


def setup(bot):
    bot.add_cog(Kpop(bot))
