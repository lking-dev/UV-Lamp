# Written by Landry M. King, 2024
# LocationObject: represents a row of the "Locations" table

class LocationObject:
    def __init__(self, data):    
        self.id = data["locationid"]
        self.address = data["locationaddress"]
        self.longitude = data["locationlongitude"]
        self.latitude = data["locationlatitude"]
        self.zipcode = data["locationzipcode"]
        self.city = data["locationcity"]
        self.state = data["locationstate"]
        self.homephone = data["locationhomephone"]

        if self.address[len(self.address) - 1] == ".":
            self.address = self.address[:-1]

        self.fulladdress = self.address + ", " + self.city + ", " + self.state + " " + str(self.zipcode)