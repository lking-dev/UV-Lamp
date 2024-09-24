import sqlite3
import os
import os.path
from container import customer
from container import order
from container import reminder

# DBConnector class
# holds all functionality for querying and updating records
class DBAccess:
    # constructor that sets up the database
    def __init__(self, pathname):
        # connect to the database and get the cursor for execution
        self.connector = sqlite3.connect(pathname)
        self.connector.row_factory = sqlite3.Row
        self.cursor = self.connector.cursor()

        # flag for the connections status
        self.connected = True

    # creates a new customer
    def addCustomer(self, customer_firstname, customer_lastname, customer_company, customer_email, customer_phone):
        sql = "INSERT INTO Customers(customerfirstname, customerlastname, customercompany, customeremail, customerphone) VALUES(?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (customer_firstname, customer_lastname, customer_company, customer_email, customer_phone))

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
        return [customer.CustomerObject(o) for o in self.cursor.fetchall() if o != None]

    # grabs all order data
    def getAllOrders(self):
        sql = "SELECT * FROM Orders;"
        self.cursor.execute(sql)
        return [order.OrderObject(o) for o in self.cursor.fetchall() if o != None]
    
    # grabs all reminder data
    def getAllReminders(self):
        sql = "SELECT * FROM Reminders;"
        self.cursor.execute(sql)
        return [reminder.ReminderObject(o) for o in self.cursor.fetchall() if o != None]
    
    # grabs all customer data
    def getCustomer(self, id):
        sql = "SELECT * FROM Customers WHERE customerid = " + str(id) + ";"
        self.cursor.execute(sql)
        return customer.CustomerObject(self.cursor.fetchone())
        
    # replaces data for a customer record
    # TODO: def updateCustomer(self, oldid, newdata):

    # replaces data for a order record
    def updateOrder(self, order):
        sql = """
            UPDATE Orders SET orderplaced = ?, orderlastchanged = ?, customerid = ?, orderlocation = ?, orderstatus = ? WHERE orderid = ?;
        """

        self.cursor.execute(sql, (order.placed, order.lastchanged, order.customerid, order.location, order.status, order.id))
        self.connector.commit()

    # replaces data for a reminder record
    # TODO: def updateReminder(self, oldid, newdata):


    # finds the id of a customer based on name and email
    # this is mainly for debug
    def searchForCustomerId(self, customer_firstname, customer_lastname, customer_email):
        sql = """
            SELECT customerid FROM Customers WHERE customerfirstname = ? AND customerlastname = ? AND customeremail = ? LIMIT 1;
        """

        self.cursor.execute(sql, (customer_firstname, customer_lastname, customer_email))
        # index of 0 corresponds to the id
        try:
            return self.cursor.fetchone()[0]
        except:
            return None
        
    def searchOrdersByCustomer(self, id):
        sql = "SELECT * FROM Orders WHERE customerid = ?;"
        self.cursor.execute(sql, [(id)])
        return [order.OrderObject(o) for o in self.cursor.fetchall() if o != None]
    
    def searchOrderById(self, id):
        sql = "SELECT * FROM Orders WHERE orderid = ?;"
        self.cursor.execute(sql, [(id)])
        return order.OrderObject(self.cursor.fetchone())
    
    # finds any reminders that pertain to a certian order
    def getReminderFromOrder(self, orderid):
        sql = "SELECT * FROM Reminders WHERE orderid = " + str(orderid) + " LIMIT 1;"
        self.cursor.execute(sql)

        data = self.cursor.fetchone()
        return reminder.ReminderObject(data)