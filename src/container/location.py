# generic order object for holding data in named fields instead of a set

class LocationObject:
    def __init__(self, data):    
        self.id = data["locationid"]
        self.address = data["locationaddress"]
        self.longitude = data["locationlongitude"]
        self.latitude = data["locationlatitude"]
        self.zipcode = data["locationzipcode"]
        self.city = data["locationcity"]
        self.state = data["locationstate"]