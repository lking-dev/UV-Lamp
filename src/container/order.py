# generic order object for holding data in named fields instead of a set

# ORDERS SCHEMA:
# orderid INTEGER PRIMARY KEY AUTOINCREMENT
# orderplaced TEXT
# orderlastchanged TEXT
# orderlocation TEXT
# orderstatus INT
# customerid INTEGER (FOREIGN KEY)

class OrderObject:
    order_statuses = {
        -1: "DELETED",
        0: "UP TO STANDARD",
        1: "IN PROCESS",
        2: "NEEDS REPLACEMENT"
    }

    def setup_none(self):
        self.id = None
        self.formattedid = None
        self.placed = None
        self.lastchanged = None
        self.customerid = None
        self.locationid = None
        self.status = None        

    def __init__(self, data = None): 
        if data == None:
            self.setup_none()
        else:       
            self.id = data["orderid"]
            self.formattedid = "{:04d}".format(self.id)
            self.placed = data["orderplaced"]
            self.lastchanged = data["orderlastchanged"]
            self.customerid = data["customerid"]
            self.locationid = data["locationid"]
            self.status = data["orderstatus"]