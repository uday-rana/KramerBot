# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import discord
from discord.ext import commands
import os
import json
import requests
from keep_alive import keep_alive
import random

my_secret = os.environ['TOKEN']
bot = commands.Bot(command_prefix='$')
seinfeld = []

def make_quote(guess):
    response = requests.get("https://seinfeld-quotes.herokuapp.com/random")
    data = json.loads(response.text)

    quote = "```" + data["quote"] + "```"
    if guess == False:
      quote = quote + ' -' + data["author"]
    quote = quote + " (Season " + data["season"] + ", Episode " + data[
        "episode"] + ')'
    return [quote, data["author"]]

def get_author():
    response = requests.get("https://seinfeld-quotes.herokuapp.com/random")
    data = json.loads(response.text)
    return data["author"]

def get_options(answer):
  author1 = get_author()
  author2 = get_author()
  list = [author1, author2, answer]
  random.shuffle(list)
  return list

@bot.command()
async def seinfeld(ctx):
    guess = False
    quote = make_quote(guess)
    await ctx.send(quote[0])

@bot.command()
async def guess(ctx):
    quote = make_quote(guess = True)
    options = get_options(quote[1])
    print(options)
    await ctx.send(quote[0])
    prompt = await ctx.send(
      f"Who said this quote?\n🇦: {options[0]}\n🇧: {options[1]}\n🇨: {options[2]}"
    )
    await prompt.add_reaction('🇦')
    await prompt.add_reaction('🇧')
    await prompt.add_reaction('🇨')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

try:
    keep_alive()
    bot.run(os.getenv("TOKEN"))
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
