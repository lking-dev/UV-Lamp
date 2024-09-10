import sqlite3
import os
import os.path
from Container import OrderObject
from Container import ReminderObject
from Container import CustomerObject

# DBConnector class
# holds all functionality for querying and updating records
class DBAccess:
    # constructor that sets up the database
    def __init__(self, pathname):
        # connect to the database and get the cursor for execution
        self.connector = sqlite3.connect(pathname)
        self.cursor = self.connector.cursor()

        # flag for the connections status
        self.connected = True

    # creates a new customer
    def addCustomer(self, customer_name, customer_email):
        sql = "INSERT INTO Customers(customername, customeremail) VALUES(?, ?)"
        self.cursor.execute(sql, (customer_name, customer_email))

    # creates a new order and links it to a customer
    def addOrder(self, customer_id, date_placed):
        sql = "INSERT INTO Orders(ordercustomer, orderplaced, orderlastchanged) VALUES(?, ?, ?);"
        self.cursor.execute(sql, (customer_id, date_placed, date_placed))

    # creates a new reminder and links it to an order
    def addReminder(self, orderid, reminder_date):
        sql = "INSERT INTO Reminders(reminderdate, orderid) VALUES(?, ?);"
        self.cursor.execute(sql, (reminder_date, orderid))

        self.connector.commit()

    # grabs all customer data
    def getAllCustomers(self):
        sql = "SELECT * FROM Customers;"
        self.cursor.execute(sql)
        return [CustomerObject.CustomerObject(o) for o in self.cursor.fetchall() if o != None]

    # grabs all order data
    def getAllOrders(self):
        sql = "SELECT * FROM Orders;"
        self.cursor.execute(sql)
        return [OrderObject.OrderObject(o) for o in self.cursor.fetchall() if o != None]
    
    # grabs all reminder data
    def getAllReminders(self):
        sql = "SELECT * FROM Reminders;"
        self.cursor.execute(sql)
        return [ReminderObject.ReminderObject(o) for o in self.cursor.fetchall() if o != None]
        
    # replaces data for a customer record
    # TODO: def updateCustomer(self, oldid, newdata):

    # replaces data for a order record
    # TODO: def updateOrder(self, oldid, newdata):

    # replaces data for a reminder record
    # TODO: def updateReminder(self, oldid, newdata):


    # finds the id of a customer based on name and email
    # this is mainly for debug
    def searchCustomerId(self, customer_name, customer_email):
        sql = """
            SELECT customerid FROM Customers WHERE customername = ? AND customeremail = ? LIMIT 1;
        """

        self.cursor.execute(sql, (customer_name, customer_email))
        # index of 0 corresponds to the id
        return self.cursor.fetchone()[0]
    
    # finds any reminders that pertain to a certian order
    def getReminderFromOrder(self, orderid):
        sql = "SELECT * FROM Reminders WHERE orderid = " + str(orderid) + " LIMIT 1;"
        self.cursor.execute(sql)

        data = self.cursor.fetchone()
        return ReminderObject.ReminderObject(data)