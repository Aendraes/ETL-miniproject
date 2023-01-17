import pandas
import requests

#Does this work?


#Url = http://swapi.dev/api/planets

response = requests.get("http://swapi.dev/api/planets")

# Convert the response data to a JSON object
data = response.json()

print(data)
