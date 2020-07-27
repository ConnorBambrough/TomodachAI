import discord

from discord.ext import commands
import random
import os

import asyncio

startup_extensions = ["kpop"]

token = open("token.txt", "r").read()  # I've opted to just save my token to a text file.



def get_prefix(client, message):

    prefixes = ['!', '=']    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix

    if not message.guild:
        prefixes = ['==']   # Only allow '==' as a prefix when in DMs, this is optional

    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(                         # Create a new bot
    command_prefix=get_prefix,              # Set the prefix
    description='A bot used for tutorial',  # Set a description for the bot
    owner_id=374886124126208000,            # Your unique User ID
    case_insensitive=True                   # Make the commands case insensitive
)

cogs = ['cogs.basic']

@bot.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'We have logged in as {bot.user}')  # notification of login.
    return


@bot.event
async def on_message(message):  # event that happens per any message.
    if message.author == bot.user:
        return
    # each message has a bunch of attributes. Here are a few.
    # check out more by print(dir(message)) for example.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    sentdex_guild = bot.get_guild(729816023938760712)

    if "sentdebot.member_count" == message.content.lower():
        await message.channel.send(f"```{sentdex_guild.member_count}```")

    elif "sentdebot.logout()" == message.content.lower():
        await bot.close()

    elif "sentdebot.community_report()" == message.content.lower():
        online, idle, offline = community_report(sentdex_guild)
        await message.channel.send(f"```Online: {online}.\nIdle/busy/dnd: {idle}.\nOffline: {offline}```")

    await bot.process_commands(message)

@bot.command()
async def cat(ctx):
    rand = random.choice(os.listdir("/root/TomodachAI/cats"))
    await ctx.send(file=discord.File("cats/" + rand))

@bot.command()
async def scatter(ctx):
    await ctx.send(file=discord.File("/root/TomodachAI/SCATTER.mp4"))

@bot.command()
async def think(ctx):
    rand = random.choice(os.listdir("/root/TomodachAI/think"))
    await ctx.send(file=discord.File("think/" + rand))

@bot.command()
async def smug(ctx):
    rand = random.choice(os.listdir("/root/TomodachAI/smug"))
    await ctx.send(file=discord.File("smug/" + rand))


@bot.command()
async def dance(ctx):
    rand = random.choice(os.listdir("/root/TomodachAI/dance"))
    try:
        await ctx.send(file=discord.File("dance/" + rand))
    except Exception:
        await ctx.send('command aint workin boss')
        return


def community_report(guild):
    online = 0
    idle = 0
    offline = 0

    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        if str(m.status) == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(token, bot=True, reconnect = True)  # recall my token was saved!
