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
answer = ''
correct_author = ''
your_answer = ''
options_dict = {}

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
  while author1 == answer:
    author1 = get_author()
  author2 = get_author()
  while author2 == answer or author2 == author1:
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
    global correct_author
    global options_dict
    quote = make_quote(guess = True)
    options = get_options(quote[1])
    correct_author = quote[1]
    print(options)
    await ctx.send(quote[0])
    options_dict = {
      'A': options[0],
      'B': options[1],
      'C': options[2]
    }
    prompt = await ctx.send(
      f"+ Who said this quote? +\n🇦: {options[0]}\n🇧: {options[1]}\n🇨: {options[2]}"
    )
    await prompt.add_reaction('🇦')
    await prompt.add_reaction('🇧')
    await prompt.add_reaction('🇨')

    for key in options_dict:
      if options_dict[key] == quote[1]:
        global answer
        answer = key

@bot.event
async def on_reaction_add(reaction, user):
  global answer
  global correct_author
  global your_answer 
  if reaction.message.channel.name == "kramer" and reaction.message.content.startswith('+'):
    if user != bot.user:
      print(reaction.message.author)
      if reaction.emoji == '🇦':
        option = 'A'
      if reaction.emoji == '🇧':
        option = 'B'
      if reaction.emoji == '🇨':
        option = 'C'

      your_answer = options_dict[option]
      if option == answer:
        await reaction.message.delete()
        await reaction.message.channel.send(f"``` {user.name.capitalize()}'s answer: {your_answer} | Correct answer: {correct_author} | {user.name} wins!```")
      else:
        await reaction.message.delete()
        await reaction.message.channel.send(f"``` {user.name.capitalize()}'s answer: {your_answer} | Correct answer: {correct_author} | {user.name} loses!```")

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
