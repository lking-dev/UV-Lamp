# Written by Landry M. King, 2024
# OrderObject: represents a row of the "Orders" table

class OrderObject:
    order_statuses = {
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

        # the SKU's of the items stored here follow the following format:
        # TUVL-<year: 1 digit><size (inch): 2 digits)><pig-tail (OPTIONAL): 1 character ('P')>"
        # so the SKU's warranty can be extracted from the 6th character of the SKU (index 5)
        self.warranty = int(self.sku[5])
        self.warrantyDays = self.warranty * 365
        self.formattedid = "{:04d}".format(self.id)