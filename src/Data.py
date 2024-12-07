# Written by Landry M. King, 2024
# Data: manages the connection to the sqlite3 local database

import sqlite3
import os
import os.path

from container.customer import CustomerObject
from container.reminder import ReminderObject
from container.order import OrderObject
from container.history import HistoryEvent
from container.location import LocationObject

# DBConnector class
# holds all functionality for querying and updating records
class Data:
    # constructor that sets up the database
    def __init__(self, pathname):
        # connect to the database and get the cursor for execution
        self.connector = sqlite3.connect(pathname)

        # THIS LINE IS VERY, VERY IMPORTANT
        # MAKES IT SO SQL RETURNS DATA AS A LIST OF DICTIONARIES INSTEAD OF LIST OF LISTS
        # ALL CODE IS BASED ON THIS FACT
        self.connector.row_factory = sqlite3.Row
        self.cursor = self.connector.cursor()

        # flag for the connections status
        self.connected = True

    def forceCommit(self):
        self.connector.commit()

    # creates a new order
    def addOrder(self, placed, original, last, customerid, status, locationid, sku):
        sql = """
            INSERT INTO Orders(
                orderplaced,
                orderlastchanged,
                orderoriginalinstall,
                orderstatus,
                ordersku,
                customerid,
                locationid
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """

        self.cursor.execute(sql, (
            placed, last, original,
            status, sku, customerid, locationid
        ))

        self.connector.commit()

        return self.cursor.lastrowid

    # creates a new reminder and links it to an order
    def addReminder(self, orderid, reminder_date):
        sql = "INSERT INTO Reminders(reminderdate, orderid) VALUES(?, ?);"
        self.cursor.execute(sql, (reminder_date, orderid))
        self.connector.commit()

        return self.cursor.lastrowid

    def addHistory(self, date, content, order):
        sql = "INSERT INTO OrderHistory(historydate, historycontent, linkedorderid) VALUES (?, ?, ?);"
        self.cursor.execute(sql, (date, content, order))
        self.connector.commit()

        return self.cursor.lastrowid
    
    def addCustomer(self, firstname, lastname, email, company, password):
        sql = "INSERT INTO Customers(customerfirstname, customerlastname, customeremail, customercompany, customerpassword) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(sql, (firstname, lastname, email, company, password))
        self.connector.commit()

        return self.cursor.lastrowid
    
    def addCustomer(self, firstname, lastname, email, company, password, locationid):
        sql = "INSERT INTO Customers(customerfirstname, customerlastname, customeremail, customercompany, customerpassword, customerlocationid) VALUES (?, ?, ?, ?, ?, ?);"
        self.cursor.execute(sql, (firstname, lastname, email, company, password, locationid))
        self.connector.commit()

        return self.cursor.lastrowid
    
    def addLocation(self, address, latitude, longitude, homephone):
        sql = """INSERT INTO Locations(
            locationaddress,
            locationlatitude,
            locationlongitude,
            locationhomephone
        ) VALUES (?, ?, ?, ?);"""

        self.cursor.execute(sql, (address, latitude, longitude, homephone))
        self.connector.commit()

        return self.cursor.lastrowid

    # removes a reminder
    def delReminder(self, reminder):
        sql = "DELETE FROM Reminders WHERE reminderid = ?;"
        self.cursor.execute(sql, [(reminder.id)])
        self.forceCommit()

    # removes an order
    def delOrder(self, order):
        sql = "DELETE FROM Orders WHERE orderid = ?;"
        self.cursor.execute(sql, [(order.id)])
        self.forceCommit()

    # grabs all customer data
    def getAllCustomers(self):
        sql = "SELECT * FROM Customers;"
        self.cursor.execute(sql)
        return [CustomerObject(o) for o in self.cursor.fetchall() if o != None]

    # grabs all order data
    def getAllOrders(self):
        sql = "SELECT * FROM Orders;"
        self.cursor.execute(sql)
        return [OrderObject(o) for o in self.cursor.fetchall() if o != None]
    
    # grabs all reminder data
    def getAllReminders(self):
        sql = "SELECT * FROM Reminders;"
        self.cursor.execute(sql)
        return [ReminderObject(o) for o in self.cursor.fetchall() if o != None]

    # find customer by id
    def searchCustomerByID(self, id):
        sql = "SELECT * FROM Customers WHERE customerid = " + str(id) + ";"
        self.cursor.execute(sql)
        return CustomerObject(self.cursor.fetchone())

    # search customer using firstname/lastname/email fields
    def customerLoginSearch(self, email, password):
        sql = "SELECT * FROM Customers WHERE customeremail = ? AND customerpassword = ? LIMIT 1;"
        self.cursor.execute(sql, (email, password))

        result = self.cursor.fetchone()
        if not result:
            return None
        return CustomerObject(result).id

    # find order by id
    def searchOrderByID(self, id):
        sql = "SELECT * FROM Orders WHERE orderid = ? LIMIT 1;"
        self.cursor.execute(sql, [(id)])

        result = self.cursor.fetchone()

        if not result:
            return None
        return OrderObject(result)

    # find reminder by id
    def searchReminderByID(self, id):
        sql = "SELECT * FROM Reminders WHERE reminderid = ? LIMIT 1;"
        self.cursor.execute(sql, [(id)])

        result = self.cursor.fetchone()

        print("SELECT * FROM Reminders WHERE reminderid = {};".format(id))

        if not result:
            return None
        return ReminderObject(result)
    
    # find location by id
    def searchLocationByID(self, id):
        sql = "SELECT * FROM Locations WHERE locationid = ? LIMIT 1;"
        self.cursor.execute(sql, [(id)])

        result = self.cursor.fetchone()

        print("SELECT * FROM Locations WHERE locationid = {} LIMIT 1;".format(id))

        if not result:
            return None
        return LocationObject(result)
    
    def searchLocationByCoordinates(self, lat, long):
        sql = """SELECT * FROM Locations WHERE locationlatitude = ? AND locationlongitude = ?;"""

        self.cursor.execute(sql, (lat, long))
        result = self.cursor.fetchone()

        if not result:
            return None
        return LocationObject(result)

    # replaces data for a customer record
    def updateCustomer(self, customer):
        sql = """
            UPDATE Customers SET
                customerfirstname = ?,
                customerlastname = ?,
                customeremail = ?,
                customercompany = ?,
                customerphone = ?   
            WHERE customerid = ?;
        """

        self.cursor.execute(sql, (
            customer.firstname,
            customer.lastname,
            customer.email,
            customer.company,
            customer.phone,
            customer.id
        ))

        self.connector.commit()

        ### UPDATE UDPATE ORDER~!~!!!!!!!!!!!!!!!
    
    # replaces data for an order record
    def updateOrder(self, order):
        sql = """
            UPDATE Orders SET 
                orderplaced = ?,
                orderlastchanged = ?,
                customerid = ?,
                orderlocation = ?,
                orderstatus = ? 
            WHERE orderid = ?;
        """

        self.cursor.execute(sql, (
            order.placed,
            order.lastchanged,
            order.customerid,
            order.location,
            order.status,
            order.id
        ))

        self.connector.commit()

    # replaces data for a reminder record
    def updateReminder(self, reminder):
        sql = """
            UPDATE Orders SET --- WHERE reminderid = ?;
        """

        self.cursor.execute(sql, (reminder.id))
        self.connector.commit()
    
    def searchOrdersForCustomer(self, customer: int):
        sql = "SELECT * FROM Orders WHERE customerid = ? LIMIT 1;"

        self.cursor.execute(sql, [(customer)])
        return [OrderObject(o) for o in self.cursor.fetchall() if o != None]
    
    # finds any reminders that pertain to a certian order
    def searchRemindersForOrder(self, orderid: int):
        sql = "SELECT * FROM Reminders WHERE orderid = ? LIMIT 1;"
        self.cursor.execute(sql, [(orderid)])
        result = self.cursor.fetchone()
        
        if not result:
            return None
        return ReminderObject(result)
    
    def searchHistoryForOrder(self, orderid: int):
        sql = "SELECT * FROM OrderHistory WHERE linkedorderid = ?;"
        self.cursor.execute(sql, [(orderid)])
        results = self.cursor.fetchall()

        if results is None:
            return None
        else:
            return [HistoryEvent(event) for event in results]