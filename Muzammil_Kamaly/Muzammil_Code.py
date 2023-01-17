import requests
import pandas as pd

# Make API request
response = requests.get("http://swapi.dev/api/people/")
data = response.json()

# Initialize empty list
planets = []

# Append data to list
for planet in data['results']:
    planets.append([planet['name'], planet['diameter'], planet['climate'], planet['terrain'], planet['surface_water'], planet['population']])

# Convert list to DataFrame
df = pd.DataFrame(planets, columns=['Name', 'Diameter', 'Climate', 'Terrain', 'Surface Water', 'Population'])

# Print table ni
print(df)

# Export to CSV
df.to_csv('planets.csv', index=False)
