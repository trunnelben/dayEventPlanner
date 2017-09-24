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

a = build_URL(search_text='new york city attractions hiking')
print(a)
response = requests.get(a)
data = requests.get(a).json()
print(data)
