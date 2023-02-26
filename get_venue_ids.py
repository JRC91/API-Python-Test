
import csv
import requests
from datetime import datetime

# Define the Ticketmaster API endpoint and parameters
endpoint = 'https://app.ticketmaster.com/discovery/v2/events.json'
apikey = '54SxRbP2JUPb4FvUtJK6pA74HOhlcrSN'

venue_ids = {}
for venue_name in venue_names:
    response = search_venues(venue_name)
    if response.status_code == 200:
        data = response.json()
        if data['_embedded']['venues']:
            venue_id = data['_embedded']['venues'][0]['id']
            venue_ids[venue_name] = venue_id
        else:
            print(f"No venue found for {venue_name}")
    else:
        print(f"Error searching venues for {venue_name}: {response.status_code}")

print(venue_ids)