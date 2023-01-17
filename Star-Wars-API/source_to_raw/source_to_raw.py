import os
import pandas as pd
import requests

# Create dir references
WORKDIR = os.path.dirname(os.path.realpath(__file__))
print(WORKDIR)

ROOTPATH = os.path.abspath(os.path.join(WORKDIR, os.pardir))
print(ROOTPATH)

source_path = ROOTPATH + "/data/testing/raw/"
print(source_path)

# # If dir not exist, otherwise #
os.makedirs(source_path)

# API Base URL
# URL = "https://swapi.dev/api/"

response = requests.get("http://swapi.dev/api/planets/")

data = response.json()

df = pd.DataFrame(data)

df.to_json(source_path + "data.json", orient = "records")