import requests
import json
import os
import datetime

# Local refs
ROOTPATH = os.path.dirname(os.path.dirname(__file__))

# Base URL
URL = "https://opendata-download-metfcst.smhi.se/"

# SMHI API Base Syntax
# /api/category/{category}/version/{version}/geotype/point/lon/{longitude}/lat/{latitude}/data.json

# Read dictionary from file created by geocode
with open(ROOTPATH+'/cleansed_to_sql/cities.txt', 'r') as fh:
    citydict = eval(fh.read())
citylistdict = {}
i = 1

for key, value in citydict.items():
    citylistdict[key] = i
    i += 1
with open(ROOTPATH+'/cleansed_to_sql/city-log.txt', 'w') as f:
    json.dump(citylistdict, f)


# Extracting/Fetching raw data by GET requests from SMHI API with the coordinates above


def get_raw_data_items():
    for i in range(len(citydict["longitude"])):
        longitude = citydict["longitude"][i]
        latitude = citydict["latitude"][i]
        city=citydict["city"][i]
        city_url = f"api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json"
        url = URL + city_url
        data = requests.get(url)
        jsonobj = json.loads(data.text)
        approvedtime = get_time(jsonobj["approvedTime"])

        with open(ROOTPATH + "/data/testing/raw/" + city + approvedtime + ".json", 'w') as f:
            json.dump(jsonobj, f, indent=3)
    print("Data Sourced")

# Reformat data from arpprovedTime


def get_time(approvedtime):
    approvedtime = datetime.datetime.strptime(
        approvedtime, '%Y-%M-%dT%H:%S:%fZ')
    approvedtime = datetime.datetime.strftime(approvedtime, '%Y-%M-%d-%H')
    return approvedtime


if __name__ == '__main__':

    get_raw_data_items()
