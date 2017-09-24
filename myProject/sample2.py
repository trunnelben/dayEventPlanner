import os
import requests
import json
ACCESS_TOKEN = 'AIzaSyDnAEuPuxGQh1DM_G3TZZDl6bhGVV2ZrvE'

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

a = build_URL(search_text='san francisco attractions')
print(a)
response = requests.get(a)
data = requests.get(a).json()
# search = "San Francisco, CA"
# print(data)
# print(search)
# print('python sample.py --location="%s"' % search)
# os.system('python sample.py --location="%s"' % search)
lat = str (data["results"][0]["geometry"]["location"]["lat"])
long = str (data["results"][0]["geometry"]["location"]["lng"])
placeName = str (data["results"][0]["name"])
print(lat)
print(long)
print(placeName)
# print('python sample.py --latitude="%s"' % lat)
# print('python sample.py --longitude="%s"' % long)
# os.system('python sample.py --latitude="%s" --longitude="%s"' % (lat, long))
os.system('python sample.py --latitude="%s" --longitude="%s"' % (lat, long))
