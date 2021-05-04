import requests
import websocket
import time
import pandas as pd
from csv import writer

ws = websocket.WebSocket()
ws.connect

res = requests.get(
    "https://127.0.0.1:2999/liveclientdata/playerlist",
    verify=False
    )

eventdata = requests.get(
    "https://127.0.0.1:2999/liveclientdata/eventdata",
    verify=False
)

# print(res)
# print(res.json())
# print(eventdata)
# print(eventdata.json())

unqiue_events = []
event_data = {}


# Run every 10 sec while playing LoL
while kill is False:
    # Get current event data from lol client
    current_event_data = requests.get(
        "https://127.0.0.1:2999/liveclientdata/eventdata",
        verify=False
    )
    # Unpackage and clean the data in json format
    clean_event_data = current_event_data.json()['Events']
    print(clean_event_data)

    # Check all events for a unqiue event
    # if event is unique save event data in csv
    for event in clean_event_data:
        key = event['EventName']
        print(key)

        # Check for unique event
        if key not in unqiue_events:
            # save local copy
            unqiue_events.append(key)
            event_data[key] = event
            # Write to csv by opening current file in append mode
            # and creating a file object for this file.
            with open('events.csv', 'a') as f_object:
                # Pass file obeject to csv.writer() to get a writer object
                writer_object = writer(f_object)

                # Create and pass a list to writer object
                # as an argument into writerow()
                writer_object(writerow([key, event]))

                # Close file object
                f_object.close()
    # Sleep for 10 sec to save on processing power.
    time.sleep(10)
