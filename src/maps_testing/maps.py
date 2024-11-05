import urllib.request
import webbrowser
import urllib
import json

api_key = "AIzaSyBQi69vJT0EvL2A2mX8aiKPCoHhELcQQvc"
type Coordinate = tuple[float, float]
type Sizing = tuple[float, float]
def construct_request(location: Coordinate, size: Sizing, fov: int, key: str = api_key):
    template = "https://maps.googleapis.com/maps/api/streetview?location={},{}&size={}x{}&fov={}&key={}"
    return template.format(location[0], location[1], size[0], size[1], fov, key)

def geolocate(address: str, key: str = api_key):
    template = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"
    formatted_address = address.replace(" ", "+")
    final = template.format(formatted_address, key)

    request = urllib.request.urlopen(final)
    json_data = json.loads(request.read())

    location = (json_data["results"][0]["geometry"]["location"]["lat"], json_data["results"][0]["geometry"]["location"]["lng"])
    return location

def main():
    request = construct_request(location = geolocate("9538 Kingston Crossing Cir., Johns Creek, GA"), size = (600, 480), fov = 60)
    request2 = construct_request(location = geolocate("5575 State Bridge Rd, Johns Creek, GA 30022"), size = (600, 480), fov = 120)
    webbrowser.open(request)
    webbrowser.open(request2)

if __name__ == "__main__":
    main()