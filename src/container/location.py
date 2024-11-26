# generic order object for holding data in named fields instead of a set

# .schema as of 11/26/2024
# CREATE TABLE IF NOT EXISTS "Locations" (
#   locationid INTEGER PRIMARY KEY AUTOINCREMENT,
#   locationaddress TEXT,
#   locationlongitude DOUBLE,
#   locationlatitude DOUBLE,
#   locationzipcode INTEGER,
#   locationcity TEXT,
#   locationstate TEXT,
#   locationhomephone TEXT
# );

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