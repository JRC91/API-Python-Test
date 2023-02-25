import requests
import json
import csv


# Get API Client
endpoint = 'https://app.ticketmaster.com/discovery/v2/venues'

params = {
    'apikey': '54SxRbP2JUPb4FvUtJK6pA74HOhlcrSN',
    'marketId': '35',
    'category': 'Music',
    'stateCode': 'NY',
    'size': '200', # Maximum number of results to return
}




# Send the HTTP request to the API endpoint
response = requests.get(endpoint, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = json.loads(response.text)

    # Print the name of each venue
    for venue in data['_embedded']['venues']:
        print(venue['name'])
else:
    # Print the error message if the request failed
    print('Error:', response.text)


