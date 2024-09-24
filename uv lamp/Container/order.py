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
        0: "ALL GOOD",
        1: "REPLACEMENT NEEDED"
    }

    def __init__(self, data):
        self.id = data["orderid"]
        self.formattedid = "{:04d}".format(self.id)
        self.placed = data["orderplaced"]
        self.lastchanged = data["orderlastchanged"]
        self.customerid = data["customerid"]
        self.location = data["orderlocation"]
        self.status = data["orderstatus"]