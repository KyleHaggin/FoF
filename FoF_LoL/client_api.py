import os
import riotwatcher as rw
import pandas as pd
from dotenv import load_dotenv
import requests
import lcu_driver as lcu

# Load .env
load_dotenv(verbose=True)

# Find/Create global variables
api_key = os.getenv('API_KEY')
watcher = rw.LolWatcher(api_key)
default_region = 'na1'

connector = lcu.Connector()



"""

"""

# @connector.ready
# async def connect(connection):
#     print('LCU API ready.')

# @connector.ready
# async def connect(connection):
#     summoner = await connection.request(
#         'get', '/lol-summoner/v1/current-summoner'
#         )
#     print(await summoner.json())


# @connector.ws.register(
#     '/lol-summoner/v1/current-summoner', event_types=('UPDATE',)
#     )
# async def icon_changed(connection, event):
#     print(f'The summoner {event.data["displayName"]} was updated.')


# @connector.ws.register('/lol-champ-select/v1/session')
# async def champ_selected(connection, event):
#     print(f'Connection Data /n')
#     print(type(event))
#     print(event.data)


@connector.close
async def disconnect(connection):
    print('LCU API disconnected')

connector.start()
