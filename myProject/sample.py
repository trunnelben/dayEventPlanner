# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.
Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = 'xPE3z3YRe2CWKyYjjICneQ'
CLIENT_SECRET = 'yVHYkskJkJMV4DHHtRqjoYXUqW1pDYK7NVrp15nNHuvReudFutMU8w1JdruvGX5V'


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
# DEFAULT_LOCATION = 'San Francisco, CA'
DEFAULT_LATITUDE = '1.0'
DEFAULT_LONGITUDE = '1.0'
DEFAULT_SORT_BY = 'review_count'
DEFAULT_RADIUS = '1600' #radius of 1.0 miles
SEARCH_LIMIT = 10


def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))

    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    abc = urllib.unquote(url)
    # print(abc)
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    # print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, term, latitude, longitude, sort_by, radius):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude.replace(' ', '+'),
        'longitude': longitude.replace(' ', '+'),
        'sort_by': sort_by.replace(' ', '+'),
        'radius': radius.replace(' ', '+'),
        'limit': SEARCH_LIMIT
        # """so this is returning the right amount of searches
        # it is now showing 10 results when I print the response. Now I just
        # want it to pull the top 3 of these not just top 1
        # """
    }
    response = request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)
    # """print(response)
    # """
    return response


def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)


def query_api(term, latitude, longitude, sort_by, radius):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, term, latitude, longitude, sort_by, radius)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, latitude, longitude, sort_by, radius))
        return
    i = 0
    while(i <= 1):
        business_id = businesses[i]['id']

        # print(u'{0} businesses found, querying business info ' \
        #     'for the top result "{1}" ...'.format(
        #         len(businesses), business_id))
        response = get_business(bearer_token, business_id)

        # print(u'Result for business "{0}" found:'.format(business_id))
        # for the second mexican restuarant this does not work becasue
        # there is an escape character it has the N with a tilde
        name = str (response["name"])
        rating = str (response["rating"])
        reviewCount = str (response["review_count"])
        foodType = (response["categories"][0]["title"])
        #pprint.pprint(response, indent=2)
        print("restuarant " + str (i) + ":")
        print("place = " + name)
        print("food type = " + foodType)
        print("Rating = " + rating)
        print("Reviews = " + reviewCount)
        print()
        i = i+1

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-la', '--latitude', dest='latitude',
                        default=DEFAULT_LATITUDE, type=str,
                        help='Search longitude (default: %(default)s)')
    parser.add_argument('-lo', '--longitude', dest='longitude',
                        default=DEFAULT_LONGITUDE, type=str,
                        help='Search longitude (default: %(default)s)')
    parser.add_argument('-sb', '--sort_by', dest='sort_by',
                        default=DEFAULT_SORT_BY, type=str,
                        help='Search sort value (default: %(default)s)')
    parser.add_argument('-r', '--radius', dest='radius',
                        default=DEFAULT_RADIUS, type=str,
                        help='Search sort value (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.latitude, input_values.longitude, input_values.sort_by, input_values.radius)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
