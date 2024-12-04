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