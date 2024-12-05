# Written by Landry M. King, 2024
# GoogleMapsAPI: routines for working with the Google Maps API

import urllib.request
import webbrowser
import urllib
import json
from Config import Config

from container.order import OrderObject
from container.history import HistoryEvent
from container.location import LocationObject
from container.customer import CustomerObject
from container.reminder import ReminderObject

def constructStreetviewRequest(location, size, fov: int):
    api_key = Config().getGoogleCreds()
    template = "https://maps.googleapis.com/maps/api/streetview?location={},{}&size={}x{}&fov={}&key={}"
    return template.format(location[0], location[1], size[0], size[1], fov, api_key)

def geolocateAddress(address: str):
    api_key = Config().getGoogleCreds()
    template = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"
    formatted_address = address.replace(" ", "+")
    final = template.format(formatted_address, api_key)

    request = urllib.request.urlopen(final)
    json_data = json.loads(request.read())

    location = (json_data["results"][0]["geometry"]["location"]["lat"], json_data["results"][0]["geometry"]["location"]["lng"])
    return location

# returns a google maps url for a location object
def constructMapsURL(location: LocationObject):
    template = "https://www.google.com/maps/search/?api=1&query={}"

    # this is a lot of formatting stuff to appease the google maps API

    tmp = location.address
    if tmp[len(tmp) - 1] == ".":
        tmp = tmp[:-1]
    location.address = tmp

    strings = [location.address, location.city, location.state, str(location.zipcode)]
    builder = ""

    for i, string in enumerate(strings):
        components = string.split()
        for j, component in enumerate(components):
            builder += component
            if (j == len(components) - 1) and (i != len(strings) - 1):
                builder += ","
            if (j != len(components) - 1) and (i != len(strings) - 1):
                builder += "+"

    request = template.format(builder)

    return request