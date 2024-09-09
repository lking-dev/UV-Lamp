import sqlite3
import os
import os.path

# DBConnector class
# holds all functionality for querying and updating records
class DBConnector:
    # constructor that sets up the database
    def __init__(self, pathname = "reminders.db"):
        # remove the previous copy if applicable
        self.removeDatabase()

        # connect to the database and get the cursor for execution
        self.connector = sqlite3.connect(pathname)
        self.cursor = self.connector.cursor()

        # flag for the connections status
        self.connected = True

        # register the three needed tables
        self.makeTables()


    def makeTables(self):
        if not self.connected:
            print("[DEBUG] makeTables failed, no connection to db")
            return

        # dates are stored as MM/DD/YYYY in a sqlite TEXT column


        # stores all the customers data, used for sending emails later
        customer_sql = """
            CREATE TABLE Customers (
                customerid INTEGER PRIMARY KEY AUTOINCREMENT,
                customername VARCHAR(64),
                customeremail VARCHAR(64)
            );
        """

        # stores data about the original order, and when it was last replaced    
        orders_sql = """
            CREATE TABLE Orders (
                orderid INTEGER PRIMARY KEY AUTOINCREMENT,
                ordercustomer INTEGER,
                orderplaced TEXT,
                orderlastchanged TEXT,
                FOREIGN KEY(ordercustomer) REFERENCES Customers(customerid)
            );
        """

        # holds the queue of all reminders waiting to be sent and when
        reminders_sql = """
            CREATE TABLE Reminders (
                reminderid INTEGER PRIMARY KEY AUTOINCREMENT,
                reminderdate TEXT,
                reminderorder INTEGER,
                FOREIGN KEY(reminderorder) REFERENCES Orders(orderid)
            );
        """

        # create all three tables.
        # im just recreating the database every run while still in early dev
        self.cursor.execute(customer_sql)
        self.cursor.execute(orders_sql)
        self.cursor.execute(reminders_sql)

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
        sql = "INSERT INTO Reminders(reminderdate, reminderorder) VALUES(?, ?);"
        self.cursor.execute(sql, (reminder_date, orderid))
    
    # finds any reminders that pertain to a certian order
    def getReminderFromOrder(self, orderid):
        sql = "SELECT * FROM Reminders WHERE reminderorder = " + str(orderid) + " LIMIT 1;"
        self.cursor.execute(sql)

        data = self.cursor.fetchone()
        return data

    # for debug, removes previous copy of database
    def removeDatabase(self, pathname = "reminders.db"):
        if os.path.isfile(pathname):
            os.remove(pathname)