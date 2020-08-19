import os
import riotwatcher as rw
import pandas as pd
from dotenv import load_dotenv

# Load .env
load_dotenv(verbose=True)

# Find/Create global variables
api_key = os.getenv('API_KEY')
watcher = rw.LolWatcher(api_key)
default_region = 'na1'


# RIOT API Test function
def test():
    # Create summoner information to test with. Julz in this case.
    test_summoner = watcher.summoner.by_name(
        default_region, 'OnceWeak'
        )
    test_ranked_stats = watcher.league.by_summoner(
        default_region, test_summoner['id']
        )

    # Print information to command line
    print(test_summoner)
    print(' ')
    print(test_ranked_stats)


# Function to access any summoner by name on the na1 server shard
def summoner_information(summoner_name, region=default_region):
    # Find summoner information based on summoner name
    summoner = watcher.summoner.by_name(region, summoner_name)
    summoner_ranked = watcher.league.by_summoner(region, summoner['id'])

    # Return the json responce from API
    return summoner, summoner_ranked


# Run tests if this file is run directly.
if __name__ == "__main__":
    test()
