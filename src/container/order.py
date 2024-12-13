# Written by Landry M. King, 2024
# OrderObject: represents a row of the "Orders" table

import Maps
import Config

class OrderObject:
    order_statuses = {
        0: "UP TO STANDARD",
        1: "IN PROCESS",
        2: "REPLACEMENT SOON",
        3: "NEEDS REPLACEMENT"
    }

    def __init__(self, data): 
        self.id = data["orderid"]
        self.placed = data["orderplaced"]
        self.lastchanged = data["orderlastchanged"]
        self.status = data["orderstatus"]
        self.address = data["orderaddress"]
        self.latitude = data["orderlatitude"]
        self.longitude = data["orderlongitude"]
        self.originalinstall = data["orderoriginalinstall"]
        self.sku = data["ordersku"]
        self.customerid = data["customerid"]
        self.warranty = data["orderwarranty"]
        self.homephone = data["orderhomephone"]

        self.formattedid = "{:04}".format(self.id)

        self.streetviewLink = Maps.constructStreetviewRequest(self.latitude, self.longitude, 600, 480, 80)
        self.locationLink = Maps.constructMapsURL(self.address)

    def getStatus(self):
        return OrderObject.order_statuses[self.status]

    def getWarranty(self):
        builder = str(self.warranty) + " Year"
        if self.warranty > 1: 
            builder += "s"
        return builder