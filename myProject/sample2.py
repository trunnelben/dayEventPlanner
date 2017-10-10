import os
import requests
import json
import argparse
ACCESS_TOKEN = 'AIzaSyCHw1SncshAFT3ry2n0poQGR4EArdx6I5Q'

import urllib

def build_URL(search_text='',types_text=''):
    base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'     # Can change json to xml to change outp$
    key_string = '?key='+ACCESS_TOKEN                                           # First think after the base_url starts$
    query_string = '&query='+urllib.quote(search_text)
    sensor_string = '&sensor=false'                                             # Presumably you are not getting locati$
    type_string = ''
    if types_text!='':
        type_string = '&types='+urllib.quote(types_text)                        # More on types: https://developers.goo$
    url = base_url+key_string+query_string+sensor_string+type_string
    return url
parser = argparse.ArgumentParser()
parser.add_argument('-st', '--searchterm', dest='searchterm', type=str)
input_values = parser.parse_args()

a = build_URL(search_text=input_values.searchterm)
# print(a)
response = requests.get(a)
data = requests.get(a).json()


# search = "San Francisco, CA"
# print(data)
# print(search)
# print('python sample.py --location="%s"' % search)
# os.system('python sample.py --location="%s"' % search)
i = 0
while(i <= 2):
    lat = str (data["results"][i]["geometry"]["location"]["lat"])
    long = str (data["results"][i]["geometry"]["location"]["lng"])
    placeName = str (data["results"][i]["name"])
    print("THING TO DO:")
    # print("latitude = " + lat)
    # print("longitude = " + long)
    print("Attraction = " + placeName)
    print("")
    print("RESTUARANTS:")
    print("")
# print('python sample.py --latitude="%s"' % lat)
# print('python sample.py --longitude="%s"' % long)
# os.system('python sample.py --latitude="%s" --longitude="%s"' % (lat, long))
    os.system('python sample.py --latitude="%s" --longitude="%s"' % (lat, long))
    i = i + 1
