# generic order object for holding data in named fields instead of a set

# ORDERS SCHEMA:
# orderid INTEGER PRIMARY KEY AUTOINCREMENT
# orderplaced TEXT
# orderlastchanged TEXT
# customerid INTEGER (FOREIGN KEY)

class OrderObject:
    def __init__(self, data):
        self.id = data[0]
        self.placed = data[1]
        self.lastchanged = data[2]
        self.customerid = data[3]