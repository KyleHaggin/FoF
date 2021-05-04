import sys
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from dateutil.parser import parse
import pytz
import requests

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
    # Reint global variables
    global catgirl_count
    catgirl_count = 0
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


# Call "help" to get details of different functions.
@client.command(name='Help', aliases=[
    'command_help', 'h', 'helper', 'command help'
    ])
async def command_help(ctx, *command):

    # Convert tuple to string.
    command = ''.join(command)
    command.lower()

    # List of possible commands
    commands = ['ping', 'summoner rank', 'convert time', 'command help']

    if command is '':
        await ctx.send(
                       'Current commands: \n'
        )
        for c in commands:
            await ctx.send(str(c) + '\n')
        return None

    # Commands with a list of possible aliases.
    ping = ['ping']
    summoner = ['summoner', 'Summoner Info']
    convert = ['convert', 'convert_time', 'convert time']
    helper = ['h', 'help', 'helper', 'command help', 'command_help']

    # Print string with the command format and expected results of each command
    if command in ping:
        await ctx.send(
                       'Ping command. \n'
                       'Command format: !ping \n'
                       'Expected result: Ping in milliseconds.'
                       )
    elif command in summoner:
        await ctx.send(
                       'Summoner rank command. \n'
                       'Command format: !summoner \\*\"summoner name\"\\* \n'
                       'Expected result: '
                       '\\*Summoner name\\* currently has the '
                       'solo queue rank of \\*summoner\'s rank\\*'
                       )
    elif command in convert:
        await ctx.send(
                       'Convert time command. \n'
                       'Command format: !convert '
                       '\\*time\\* or \\*\"datetime\"\\* '
                       '\\*timezone to convert to\\* \\*timezone to convert '
                       'from (default PST)\\* \n'
                       'Expected result: \\*converted datetime\\*'
                       )
    elif command in helper:
        await ctx.send(
                       'Help command. \n'
                       'Command format: !h \\*command name\\* \n'
                       'Expected result: \\*Command name. Command call format.'
                       ' Command\'s expected result\\*'
        )
    else:
        await ctx.send(
                       '{0} is currently not a command.'
                       'If you believe this is an error, '
                       'contact a FoF admin.'.format(command)
        )


# Proof of concept discord command.
@client.command(name='Ping', aliases=['ping'])
async def ping(ctx):
    print('Ping check.')
    await ctx.send(f'This bot\'s ping is {round(client.latency * 1000)}ms.')


# Take summoner name and display their rank and rank emblem.
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
            emblem_path = '{0}\\ranked_emblems\\{1}.png'.format(
                                str(folder_path), summoner_info_clean[1])
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


# Take summoner name and display their rank and rank emblem.
@client.command(name='Convert Time', aliases=['convert', 'convert_time'])
async def convert_time(ctx, original_time, convert_to, convert_from='pst'):

    # Convert timezone string to lowercase
    convert_to.lower()
    convert_from.lower()

    # Timezones and aliases
    pst = ['pst', 'pacific']
    est = ['est', 'eastern']
    cst = ['cst', 'central']
    mst = ['mst', 'mountain']
    hst = ['hst', 'hawaii']

    # Original timezone
    if convert_from in pst:
        con_from = pytz.timezone('US/Pacific')
    elif convert_from in est:
        con_from = pytz.timezone('US/Eastern')
    elif convert_from in cst:
        con_from = pytz.timezone('US/Central')
    elif convert_from in mst:
        con_from = pytz.timezone('US/Mountain')
    elif convert_from in hst:
        con_from = pytz.timezone('US/Hawaii')

    # Convert timezone
    if convert_to in pst:
        con_to = pytz.timezone('US/Pacific')
    elif convert_to in est:
        con_to = pytz.timezone('US/Eastern')
    elif convert_to in cst:
        con_to = pytz.timezone('US/Central')
    elif convert_to in mst:
        con_to = pytz.timezone('US/Mountain')
    elif convert_to in hst:
        con_to = pytz.timezone('US/Hawaii')

    # Parse timezone
    date = parse(original_time)

    # Convert to UTC standard
    date_from = con_from.localize(date)
    date_utc = date_from.astimezone(pytz.utc)

    # Convert to wanted timezone
    date_final = date_utc.astimezone(con_to)

    await ctx.send(str(date_final.date()) + ' ' + str(date_final.time()))


# Joke command
@client.command(
    name='catgirl',
    aliases=[' catgirl', 'faeles', 'Faeles', 'fae', 'Catgirl']
    )
async def catgirl(ctx):
    response = requests.get('https://nekos.life/api/neko')
    image_link = response.json()
    await ctx.send(f'{image_link["neko"]}')
    global catgirl_count
    catgirl_count += 1


# Joke command.
@client.command(
    name='catgirlcount', aliases=[
        'faelescount', 'faecount', 'Faelescount',
        'faelescounter', 'Faelescounter'
        ]
    )
async def catgirlcount(ctx):
    global catgirl_count
    await ctx.send(
        f'There have been {catgirl_count} catgirls since bot restart.'
        )

client.run(token)
