# Written by Landry M. King, 2024
# LocationObject: represents a row of the "Locations" table

class LocationObject:
    def __init__(self, data):    
        self.id = data["locationid"]
        self.address = data["locationaddress"]
        self.longitude = data["locationlongitude"]
        self.latitude = data["locationlatitude"]
        self.homephone = data["locationhomephone"]