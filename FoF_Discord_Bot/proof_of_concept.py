import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load .env
load_dotenv(verbose=True)

# Get tokens and credentials from .env
token = os.getenv('FoF_BOT_TOKEN')

# Set discord client command prefix
# (what people type as a activation for a bot command)
client = commands.Bot(command_prefix='!')


# On ready event (brings bot online in the server)
@client.event
async def on_ready():
    print('Bot is Ready')


# Create proof of concept message return for the bot
@client.event
async def on_message(message):
    # Set bot to ignore messages from itself
    if message.author == client.user:
        return

    # If bot sees a message that starts with Hello, reply 'Hello!' back
    if message.content.startswith('Hello'):
        await message.channel.send('Hello!')

    await client.process_commands(message)

# Proof of concept discord command.
@client.command(name='Ping', aliases=['ping'])
async def ping(ctx):
    print('Ping check.')
    await ctx.send(f'This bot\'s ping is {round(client.latency * 1000)}ms.')

client.run(token)
