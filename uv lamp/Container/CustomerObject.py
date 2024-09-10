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
        self.id = data[0]
        self.firstname = data[1]
        self.lastname = data[2]
        self.company = data[3]
        self.email = data[4]
        self.phone = data[5]