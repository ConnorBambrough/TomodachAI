import discord
import urllib.request as req
import os
from discord.ext import commands
import random
import praw

token = open("token.txt", "r").read()  # I've opted to just save my token to a text file.

reddit = praw.Reddit(client_id="ZPKPPTv0oiUbOQ",
                     client_secret="lzjMIcEG5FzGls5sZ4DuQsgNnD4",
                     user_agent="Connors TomodachAI scrawling reddit")


def get_prefix(client, message):
    prefixes = ['!', '=']  # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix

    if not message.guild:
        prefixes = ['==']  # Only allow '==' as a prefix when in DMs, this is optional

    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(  # Create a new bot
    command_prefix=get_prefix,  # Set the prefix
    description='Connors shit ass bot',  # Set a description for the bot
    owner_id=374886124126208000,  # Your unique User ID
    case_insensitive=True  # Make the commands case insensitive
)

cogs = ['cogs.basic', 'cogs.kpop', 'cogs.imgspam']


@bot.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'We have logged in as {bot.user}')  # notification of login.
    for cog in cogs:
        bot.load_extension(cog)
    return


@bot.event
async def on_message(message):  # event that happens per any message.
    if message.author == bot.user:
        return
    # each message has a bunch of attributes. Here are a few.
    # check out more by print(dir(message)) for example.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    sentdex_guild = bot.get_guild(729816023938760712)

    if "tomodachi.member_count" == message.content.lower():
        await message.channel.send(f"```{sentdex_guild.member_count}```")

    elif "tomodachi.logout()" == message.content.lower():
        await bot.close()

    elif "tomodachi.community_report()" == message.content.lower():
        online, idle, offline = community_report(sentdex_guild)
        await message.channel.send(f"```Online: {online}.\nIdle/busy/dnd: {idle}.\nOffline: {offline}```")

    elif message.content == '!stop':
        await bot.logout()

    #Links the current front page post in a particular subreddit.
    if message.content.startswith('currentTop'):
        if ' ' in  message.content:
            discordSubreddit = str(message.content).split(' ')[1]

            try:
                subreddit = reddit.subreddit(discordSubreddit)

                imageUrls = []
                for submission in subreddit.hot(limit=100):
                    if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
                        imageUrls.append(submission.url)

                    if not submission.stickied:
                        discordReceive = {'title': submission.title, 'link': f'https:/www.reddit.com{submission.permalink}'}
                        discordReceive = discordReceive['title'] + '\n' + discordReceive['link']
                        await message.channel.send(discordReceive)

                        discordReceive = imageUrls[random.randint(0, len(imageUrls) - 1)]
                        req.urlretrieve(discordReceive, 'tempDiscord.jpg')
                        fullPath = os.path.join(os.getcwd(), 'tempDiscord.jpg')
                        file = discord.File(fullPath)

                        await message.channel.send(discordReceive)
                        os.remove('tempDiscord.jpg')
                        break

            except Exception as e:
                print(e)
                await message.channel.send('This sub is either banned, quarantined, or does not exist.')


    #Sends random image from a subreddit.
    if message.content.startswith('randomImage'):
        if ' ' in  message.content:
            discordSubreddit = str(message.content).split(' ')[1]

            try:
                subreddit = reddit.subreddit(discordSubreddit)

                imageUrls = []
                for submission in subreddit.hot(limit=100):
                    if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
                        imageUrls.append(submission.url)

                discordReceive = imageUrls[random.randint(0,len(imageUrls) - 1)]
                req.urlretrieve(discordReceive, 'tempDiscord.jpg')
                fullPath = os.path.join(os.getcwd(), 'tempDiscord.jpg')

                file = discord.File(fullPath)
                await message.channel.send(file=file)

                os.remove('tempDiscord.jpg')

            except Exception as e:
                print(e)
                await message.channel.send('This sub is either banned, quarantined, or does not exist.')



    await bot.process_commands(message)


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


@bot.command()
async def top10(ctx):
    for submission in reddit.subreddit("dankmemes").hot(limit=10):
        await ctx.channel.send(submission.title)


bot.run(token, bot=True, reconnect=True)  # recall my token was saved!
