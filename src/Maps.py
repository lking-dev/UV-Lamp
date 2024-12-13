# Written by Landry M. King, 2024
# GoogleMapsAPI: routines for working with the Google Maps API

import urllib.request
import webbrowser
import urllib
import json
import googlemaps
from Config import Config


def constructStreetviewRequest(lat, long, width, height, fov: int):
    api_key = Config().getGoogleCreds()
    template = "https://maps.googleapis.com/maps/api/streetview?location={},{}&size={}x{}&fov={}&key={}"
    return template.format(lat, long, width, height, fov, api_key)

# validates an addresses validity, returns None if bad address
def validateAddress(crude_address):
    client = googlemaps.Client(key = Config().getGoogleCreds())
    results = client.addressvalidation(crude_address, regionCode = 'US')
    
    if results["result"]["verdict"]["validationGranularity"] == "PREMISE":
        return results["result"]["address"]["formattedAddress"]
    else:
        return None

def geolocateAddress(address):
    client = googlemaps.Client(key = Config().getGoogleCreds())
    results = client.addressvalidation(address, regionCode = 'US')

    if results["result"]["verdict"]["validationGranularity"] == "PREMISE":
        return (results["result"]["geocode"]["location"]["latitude"], results["result"]["geocode"]["location"]["longitude"])
    else:
        return None

# returns a google maps url for a location object
def constructMapsURL(address):
    template = "https://www.google.com/maps/search/?api=1&query={}"
    builder = ""

    # this is a lot of formatting stuff to appease the google maps API
    components = address.split()
    for i, component in enumerate(components):
        builder += component
        if (i != len(components) - 1):
            builder += "+"

    request = template.format(builder)

    return request