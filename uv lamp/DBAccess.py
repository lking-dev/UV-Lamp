import sqlite3
import os
import os.path

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

    # inserts a new customer record
    def addCustomer(self, customer_name, customer_email):
        sql = "INSERT INTO Customers(customername, customeremail) VALUES(?, ?)"
        self.cursor.execute(sql, (customer_name, customer_email))

    # finds the id of a customer based on name and email
    # this is mainly for debug
    def searchCustomerId(self, customer_name, customer_email):
        sql = """
            SELECT customerid FROM Customers WHERE customername = ? AND customeremail = ? LIMIT 1;
        """

        self.cursor.execute(sql, (customer_name, customer_email))
        # index of 0 corresponds to the id
        return self.cursor.fetchone()[0]
    
    # adds a new order and links it to a customer
    def addOrder(self, customer_id, date_placed):
        sql = "INSERT INTO Orders(ordercustomer, orderplaced, orderlastchanged) VALUES(?, ?, ?);"
        self.cursor.execute(sql, (customer_id, date_placed, date_placed))

    # returns all orders in the database
    def getOrders(self):
        sql = "SELECT * FROM Orders"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    # links a new reminder to an order
    def addReminder(self, orderid, reminder_date):
        sql = "INSERT INTO Reminders(reminderdate, orderid) VALUES(?, ?);"
        self.cursor.execute(sql, (reminder_date, orderid))

        self.connector.commit()
    
    # finds any reminders that pertain to a certian order
    def getReminderFromOrder(self, orderid):
        sql = "SELECT * FROM Reminders WHERE orderid = " + str(orderid) + " LIMIT 1;"
        self.cursor.execute(sql)

        data = self.cursor.fetchone()
        return data