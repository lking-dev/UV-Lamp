# generic order object for holding data in named fields instead of a set

# .schema as of 11/26/2024
# CREATE TABLE Orders (
#   orderid INTEGER PRIMARY KEY AUTOINCREMENT,
#   orderplaced TEXT,
#   orderlastchanged TEXT,
#   customerid INTEGER,
#   orderstatus INTEGER,
#   locationid INTEGER,
#   orderoriginalinstall TEXT, 
#   ordersku TEXT, 
#   FOREIGN KEY(customerid) REFERENCES Customers(customerid), 
#   FOREIGN KEY(locationid) REFERENCES Locations(locationid)
# );

class OrderObject:
    order_statuses = {
        -1: "DELETED",
        0: "UP TO STANDARD",
        1: "IN PROCESS",
        2: "REPLACEMENT SOON",
        3: "NEEDS REPLACEMENT"
    }

    def __init__(self, data = None): 
        self.id = data["orderid"]
        self.placed = data["orderplaced"]
        self.lastchanged = data["orderlastchanged"]
        self.originalinstall = data["orderoriginalinstall"]
        self.customerid = data["customerid"]
        self.locationid = data["locationid"]
        self.status = data["orderstatus"]
        self.sku = data["ordersku"]

        self.formattedid = "{:04d}".format(self.id)