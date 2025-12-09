# This example requires the 'members' and 'message_content' privileged intents to function.
import requests
import os
import discord
from discord.ext import commands
import random
import asyncio
from Main import *


description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    # Tell the type checker that User is filled up at this point
    assert bot.user is not None
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def video(ctx):
    lista = ["https://www.mapfre.com.mt/media/39737-scaled.jpg",
             "https://ipshealth.co.za/wp-content/uploads/2022/06/The-Importance-of-Recycling.jpg", ]
    await ctx.send(random.choice(lista))

@bot.event
async def on_message(message):
    if message.content.startswith('$Is a plastic bottle recycable?'):
        await message.channel.send("It sure is! A plastic bottle can help you to keep many things! Like liquids or to make experiments")

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    # Joined at can be None in very bizarre cases so just handle that as well
    if member.joined_at is None:
        await ctx.send(f'{member} has no join date.')
    else:
        await ctx.send(f'{member} joined {discord.utils.format_dt(member.joined_at)}')
        
@bot.command()
async def password(ctx, length: int = 8):
    await ctx.send(f"Your new password is: {gen_pass(length)}")

@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


@bot.command()
async def mem(ctx):
    img = random.choice(os.listdir("imgs"))
    with open(f"imgs/{img}", "rb") as f:
        # ¡Vamos a almacenar el archivo de la biblioteca Discord convertido en esta variable!
        picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)


def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Una vez que llamamos al comando duck, 
    el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)


"""#  $guess GAME
@bot.event
async def on_message(message):
    # Prevent bot from replying to itself
    if message.author == bot.user:
        return

    # Guessing game
    if message.content.startswith('$guess'):
        await message.channel.send("Guess a number between 1 and 10.")

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await bot.wait_for("message", check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(f"Sorry, you took too long. It was {answer}.")

        if int(guess.content) == answer:
            await message.channel.send("You are right!")
        else:
            await message.channel.send(f"Oops! The answer was {answer}.")"""


bot.run("")
