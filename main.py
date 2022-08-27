# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import discord
import os
import json
import requests
from keep_alive import keep_alive

def seinfeld(guess=False):
    response = requests.get("https://seinfeld-quotes.herokuapp.com/random")
    data = json.loads(response.text)

    quote = "```" + data["quote"] + "```"
    if guess == False:
        quote = quote + ' -' + data["author"]
    quote = quote + " (Season " + data["season"] + ", Episode " + data[
        "episode"] + ')'
    return (quote)

my_secret = os.environ['TOKEN']
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$seinfeld'):
        quote = seinfeld()
        await message.channel.send(quote)

    if message.content.startswith('$guess'):
        quote = seinfeld(True)
        await message.channel.send(quote)


try:
    keep_alive()
    client.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
