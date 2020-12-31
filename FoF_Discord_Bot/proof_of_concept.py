import sys
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pathlib import Path

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

    # Initialize the variables
    summoner_info_clean = None
    summoner = None
    summoner_ranked = None
    # Pull summoner informatin from riot_api. Raise exception if API is offline
    try:
        summoner, summoner_ranked = riot_api.summoner_information(
            summoner_name)
        print('Summoner:', summoner)
        print('Summoner_ranked: ', summoner_ranked)
    except Exception:
        print('API offline.')
        await ctx.send('Something went wrong with the API. '
                       'Please inform an admin of this.')

    # Find summoner rank from the info provided by the api.
    # If no rank exists keep summoner_info_clean as None.
    try:
        if summoner_ranked[0]['queueType'] == 'RANKED_SOLO_5x5':
            summoner_info_clean = (
                summoner['name'], summoner_ranked[0]['tier'],
                summoner_ranked[0]['rank']
                )
        elif summoner_ranked[1]['queueType'] == 'RANKED_SOLO_5x5':
            summoner_info_clean = (
                summoner['name'], summoner_ranked[1]['tier'],
                summoner_ranked[1]['rank']
                )
    except Exception:
        pass

    # If there is information in summoner,
    # that means the API was successful and something
    # should be posted to Discord.
    if summoner is not None:
        # If there is clean info, than there is a rank assocciated
        # with the Summoner. Post that rank to Discord.
        if summoner_info_clean is not None:
            await ctx.send(
                '{0} currently has the solo queue rank of {1} {2}'.format(
                    summoner_info_clean[0], summoner_info_clean[1],
                    summoner_info_clean[2]
                    ))
            folder_path = Path('FoF_LoL').resolve()
            print(folder_path)
            emblem_path = str(folder_path) + '\\ranked_emblems\\{0}.png'.format(summoner_info_clean[1])
            await ctx.send(
                file=discord.File(emblem_path)
                )

        # If there is no clean info, there is no rank assocciated
        # with the summoner. Post as such.
        else:
            await ctx.send(
                '{0} currently does not have a solo queue rank.'.format(
                    summoner_name)
                    )

client.run(token)
