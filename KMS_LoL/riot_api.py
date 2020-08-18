import os
import riotwatcher as rw
import pandas as pd
from dotenv import load_dotenv

# Load .env
load_dotenv(verbose=True)

# Find/Create global variables
api_key = os.getenv('API_KEY')
watcher = rw.LolWatcher(api_key)
region = 'na1'


def test():
    # Create summoner information to test with. Julz in this case.
    test_summoner = watcher.summoner.by_name(region, 'Rârgh')
    test_ranked_stats = watcher.league.by_summoner(region, test_summoner['id'])
    print(test_summoner)
    print(test_ranked_stats)


test()
