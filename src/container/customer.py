# generic customer object for holding data in named fields instead of a set

# CUSTOMER SCHEMA:
# customerid INTEGER PRIMARY KEY AUTOINCREMENT,
# customerfirstname TEXT
# customerlastname TEXT
# customercompany TEXT
# customeremail TEXT
# customerphone TEXT

class CustomerObject:
    def __init__(self, data):
        self.id = data["customerid"]
        self.firstname = data["customerfirstname"]
        self.lastname = data["customerlastname"]
        self.company = data["customercompany"]
        self.email = data["customeremail"]
        self.phone = data["customerphone"]

    def __eq__(self, r):
        return self.id == r.id