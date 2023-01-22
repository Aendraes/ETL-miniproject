import urllib.request, urllib.parse, urllib.error
import json
import ssl,os
import requests
import math
api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro
if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def getlocation(location_name):
    address = location_name

    if len(address) < 1: return None
    parms = dict()
    parms['address'] = address
    
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    try:
        js = json.loads(data)
    except:
        js = None
    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        
        return (None,None)
    print(location_name)
    lat=js["results"][0]["geometry"]["location"]["lat"]
    lon=js["results"][0]["geometry"]["location"]["lng"]
    lon = math.floor(lon*100000)/100000
    lat = math.floor(lat*100000)/100000
    return (lat,lon)

def open_city_list():
    citylist = ['stockholm','göteborg', 'malmö','Umeå','Lödöse','trosa']
    with open(os.path.dirname(__file__)+'/cities.txt','r') as fh:
        cities = fh.read().split(',')
    return cities

def get_multiple_locations(location_list = open_city_list()):
    citydict = {}
    citydict["city_id"] = []
    citydict["city"] = []
    citydict["country"] = []
    citydict["county"] = []
    citydict["longitude"] = []
    citydict["latitude"] = []
    id = 1

    for address in location_list:
        parms = dict()
        parms['address'] = address

        if api_key is not False: parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)
        data = requests.get(url).text
        js = json.loads(data)

        # if not js or 'status' not in js or js['status'] != 'OK':
        #     print('==== Failure To Retrieve ====')
            
        #     return (None,None)
        # print(location_name)
        for city_dict in js["results"][0]["address_components"]:
            if "locality" in city_dict["types"]:
                citydict["city"].append(city_dict["long_name"])
            if "administrative_area_level_1" in city_dict["types"]:
                citydict["county"].append(city_dict["long_name"])
            if "country" in city_dict["types"]:
                citydict["country"].append(city_dict["long_name"])
        citydict["city_id"].append(id)
        lat=js["results"][0]["geometry"]["location"]["lat"]
        lon=js["results"][0]["geometry"]["location"]["lng"]
        lon = math.floor(lon*100000)/100000
        lat = math.floor(lat*100000)/100000
        citydict["latitude"].append(lat)
        citydict["longitude"].append(lon)
        id +=1

    print(citydict)
    with open(os.path.dirname(__file__) + '/cleansed_to_sql/cities.txt', 'w') as fh:
        json.dump(citydict, fh)
