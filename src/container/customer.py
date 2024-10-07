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

    # this single line of code method maintains the codes preformance over large databases
    # used for checking if repeat customer
    # this way i can seamlessly integrate it into the python checking, not write some garbage O(n) function to check
    # which would be double the time anyways because it would run afterwords
    def __eq__(self, r):
        return self.id == r.id