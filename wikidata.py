from SPARQLWrapper import SPARQLWrapper, JSON

# Set up the Wikidata SPARQL endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Set user agent
user_agent = 'Research-Project/0.0 (james.edmunds@me.com)'

# Set up the SPARQL query with a filter for music venues in New York and a capacity range, and limit the results to 50
query = f"""
SELECT ?venueLabel ?capacity
WHERE {{
  ?venue wdt:P31 wd:Q16917; # Instance of Music Venue
         rdfs:label ?venueLabel; # Label of the Venue
         wdt:P1083 ?capacity; # Capacity of the Venue

  FILTER (lang(?venueLabel) = "en") # Filter to only English labels
}}
LIMIT 50
"""

# Set the SPARQL query and return the results as JSON
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
sparql.addCustomHttpHeader("User-Agent", user_agent)
results = sparql.query().convert()

# Extract the list of music venues and their capacities from the results
venues = [(result["venueLabel"]["value"], result["capacity"]["value"]) for result in results["results"]["bindings"]]

# Print the list of music venues and their capacities
for venue, capacity in venues:
    print(f"Venue: {venue}, Capacity: {capacity}")
