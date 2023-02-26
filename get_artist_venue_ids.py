import csv
import requests
from datetime import datetime

# Define the Ticketmaster API endpoint and parameters
endpoint = 'https://app.ticketmaster.com/discovery/v2/events.json'
apikey = '54SxRbP2JUPb4FvUtJK6pA74HOhlcrSN'

venues = []

# Load the venues from the CSV file
with open('nyc_venues_clean2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        venues.append({'name': row['venue_name'], 'capacity': row['capacity']})

# # Search for each venue and get its ID
# venue_ids = {}
# for venue_name in venues:
#     url = 'https://app.ticketmaster.com/discovery/v2/venues'
#     params = {
#         'apikey': apikey,
#         'keyword': venue_name
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if '_embedded' in data and 'venues' in data['_embedded']:
#         first_result = data['_embedded']['venues'][0]
#         venue_id = first_result['id']
#         venue_ids[venue_name] = venue_id
#     else:
#         print('No venue found for', venue_name)

# print(venue_ids)

# # Open a new file for writing
# with open('venue_ids.csv', 'w', newline='') as csvfile:
#     # Create a CSV writer object
#     writer = csv.writer(csvfile)
#
#     # Write the header row
#     writer.writerow(['venue_name', 'venue id'])
#
#     # Write the data rows
#     for venue_name, venue_id in venue_ids.items():
#         writer.writerow([venue_name, venue_id])

# # load the venue ids from the CSV file
# with open('venue_ids.csv', newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     venue_ids = {row['venue_name']: row['venue id'] for row in reader}

# Query the Ticketmaster API for each venue's ID
venue_ids = {}
for venue in venues:
    url = f"https://app.ticketmaster.com/discovery/v2/venues.json?apikey={apikey}&keyword={venue['name']}"
    response = requests.get(url)
    data = response.json()

    if data.get("_embedded") and data["_embedded"].get("venues"):
        venue_id = data["_embedded"]["venues"][0]["id"]
        venue_ids[venue['name']] = {'id': venue_id, 'capacity': venue['capacity']}
    else:
        print(f"No venue ID found for {venue['name']}")

# Get upcoming events for each venue ID and write to CSV file
with open('upcoming_events.csv', mode='w') as csv_file:
    fieldnames = ['event name', 'venue_name', 'capacity']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for venue_name, venue_data in venue_ids.items():
        url = f"https://app.ticketmaster.com/discovery/v2/events?apikey={apikey}&venueId={venue_data['id']}&sort=date%2Casc"
        response = requests.get(url)
        data = response.json()
        if '_embedded' in data and 'events' in data['_embedded'] and data['_embedded']['events']:
            event_name = data['_embedded']['events'][0]['name']
            capacity = venue_data['capacity']
            writer.writerow({'event name': event_name, 'venue_name': venue_name, 'capacity': capacity})
            print(f"Wrote upcoming event for {venue_name}")
        else:
            print(f"No upcoming events found for {venue_name}")




