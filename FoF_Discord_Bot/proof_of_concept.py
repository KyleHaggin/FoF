import sys
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# imports from other directories
sys.path.append('.')
# from FoF_LoL.riot_api import summoner_information
from FoF_LoL import database
from FoF_LoL.database import read_write_summoner_info
from FoF_LoL import riot_api

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

    # Passes messages to command processing.
    # Without this processing messages with commands will not be read.
    # This must always go after any message content parsing.
    await client.process_commands(message)

# Proof of concept discord command.
@client.command(name='Ping', aliases=['ping'])
async def ping(ctx):
    print('Ping check.')
    await ctx.send(f'This bot\'s ping is {round(client.latency * 1000)}ms.')


@client.command(name='Summoner Info', aliases=['summoner'])
async def summoner_info(ctx, summoner_name):

    summoner, summoner_ranked = riot_api.summoner_information(summoner_name)

    if summoner_ranked[0]['queueType'] == 'RANKED_SOLO_5x5':
        summoner_info_clean = (summoner['name'], summoner_ranked[0]['tier'],
                               summoner_ranked[0]['rank'])
    elif summoner_ranked[1]['queueType'] == 'RANKED_SOLO_5x5':
        summoner_info_clean = (summoner['name'], summoner_ranked[1]['tier'],
                               summoner_ranked[1]['rank'])

    # summoner_info_clean = read_write_summoner_info(summoner_name)
    await ctx.send(summoner_info_clean)
    # await ctx.send(summoner_information(summoner_name))

client.run(token)
