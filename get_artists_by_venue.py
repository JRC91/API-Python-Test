import csv
import requests
from datetime import datetime

# Define the Ticketmaster API endpoint and parameters
endpoint = 'https://app.ticketmaster.com/discovery/v2/events.json'
apikey = '54SxRbP2JUPb4FvUtJK6pA74HOhlcrSN'


# Open the CSV file containing the list of venues
with open('ny_venues.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['venue_name', 'capacity', 'venue_type'])
    for row in reader:
        # Construct the query parameters
        params = {
            'apikey': apikey,
            'venueId': row['venue_name'],
            'size': 1, # Only return the next event
            'sort': 'date,asc' # Sort events by date in ascending order
        }

        # Send the API request
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print(data)
            # Check if the response contains any events
            if data['_embedded']['events']:
                # Extract the artist name(s) from the first event in the response
                artist_names = [artist['name'] for artist in data['_embedded']['events'][0]['_embedded']['attractions']]

                # Extract the event date and time from the first event in the response
                event_datetime = datetime.fromisoformat(data['_embedded']['events'][0]['dates']['start']['dateTime'])

                # Print the event information
                print(f"Next event at {row['Venue Name']}:")
                print(f"  Capacity: {row['Capacity']}")
                print(f"  Venue type: {row['Venue Type']}")
                print(f"  Date and time: {event_datetime.strftime('%A, %B %d, %Y %I:%M %p')}")
                print(f"  Artist(s): {', '.join(artist_names)}")
            else:
                print(f"No upcoming events at {row['Venue Name']}")
        else:
            # Print the error message if the request failed
            print(f"Error {response.status_code}: {response.text}")

