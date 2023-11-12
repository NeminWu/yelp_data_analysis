# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to https://docs.developer.yelp.com/docs/get-started for the API
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


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
# Set your API key
DEFAULT_API_KEY = "ZsxFH1wr2C-cj6r4QY5-_EcRaQBMCSWm4gmrpx6SqmHAxfSEt_8QDKckHnJ1hSo4dWs3sLeqQ5RIdkPdhsmLSsob-WBvM5wU73rf1xxeO2lwqohNFE8511pzrSQcZXYx"
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Atlanta, GA'
SEARCH_LIMIT = 2


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
        #'Content - Language': 'en - US',
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, business_id):  # , term
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        business_id (str): The search business_id passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    review_path = BUSINESS_PATH + business_id
    url_params = {
        #'term': term.replace(' ', '+'),
        #'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'business_id_or_alias': business_id,
        'Content - Language': 'en - US'
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def query_api(api_key, business_id, output_file):  # , term
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(api_key, business_id)  # , term
    print("response", response)

    reviews = response.get('reviews')

    if not reviews:
        print(u'No reviews for POI in {0} found.'.format(business_id))
        return

    # Save the response to a JSON file
    with open(output_file, 'a') as json_file:
        for review in review:
            json.dump(reviews, json_file, indent=2)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-k', '--api_key', dest='api_key',
                        default=DEFAULT_API_KEY, type=str,
                        help='API_KEY')
    # parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,type = str, help = 'Search term (default: %(default)s)')
    parser.add_argument('-l', '--business_id', dest='business_id',
                        default=None, type=str,
                        help='Search business_id')
    parser.add_argument('-o', '--output', dest='output',
                        default='output.json', type=str,
                        help='Output JSON file (default: output.json)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.api_key, input_values.business_id,
                  input_values.output)  # , input_values.term
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
