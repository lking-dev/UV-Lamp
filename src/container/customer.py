# Written by Landry M. King, 2024
# CustomerObject: represents a row of the "Customers" table
# Note: Customer is synonymous with Contractor


class CustomerObject:
    def __init__(self, data):
        self.id = data["customerid"]
        self.firstname = data["customerfirstname"]
        self.lastname = data["customerlastname"]
        self.company = data["customercompany"]
        self.email = data["customeremail"]
        self.password = data["customerpassword"]
        self.location = data["customerlocationid"]

        if self.firstname and self.lastname:
            self.fullname = self.firstname + " " + self.lastname

    # this single line of code method maintains the codes preformance over large databases
    # used for checking if repeat customer
    # this way i can seamlessly integrate it into the python checking, not write some garbage O(n) function to check
    # which would be double the time anyways because it would run afterwords
    def __eq__(self, r):
        return self.id == r.id