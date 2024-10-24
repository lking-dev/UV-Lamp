import sqlite3
import os
import os.path
from pathlib import Path
from container.customer import CustomerObject
from container.reminder import ReminderObject
from container.order import OrderObject

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

    #########################
    ###   ADD FUNCTIONS   ###
    #########################

    # creates a new order
    def addOrder(self, order: OrderObject):
        sql = """
            INSERT INTO Orders(
                orderplaced,
                orderlastchanged,
                customerid,
                orderlocation,
                orderstatus
            ) VALUES (?, ?, ?, ?, ?);
        """

        self.cursor.execute(sql, (
            order.placed,
            order.lastchanged,
            order.customerid,
            order.location,
            order.status,
        ))

        self.connector.commit()

    # creates a new reminder and links it to an order
    def addReminder(self, orderid, reminder_date):
        sql = "INSERT INTO Reminders(reminderdate, orderid) VALUES(?, ?);"
        self.cursor.execute(sql, (reminder_date, orderid))

        self.connector.commit()

    ############################
    ###   DELETE FUNCTIONS   ###
    ############################
    

    # removes a reminder
    def delReminder(self, reminder):
        sql = "DELETE FROM Reminders WHERE reminderid = ?;"
        self.cursor.execute(sql, [(reminder.id)])
        self.forceCommit()

    #############################
    ###   GET ALL FUNCTIONS   ###
    #############################

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

    ############################
    ###   SEARCH FUNCTIONS   ###
    ############################

    # find customer by id
    def searchCustomerByID(self, id):
        sql = "SELECT * FROM Customers WHERE customerid = " + str(id) + ";"
        self.cursor.execute(sql)
        return CustomerObject(self.cursor.fetchone())

    # search customer using firstname/lastname/email fields
    def searchCustomerByFields(self, firstname, lastname, email):
        sql = "SELECT * FROM Customers WHERE customerfirstname = ? AND customerlastname = ? AND customeremail = ? LIMIT 1;"
        self.cursor.execute(sql, (firstname, lastname, email))

        result = self.cursor.fetchone()
        if not result:
            return None
        return CustomerObject(result)

    # find order by id
    def searchOrderByID(self, id):
        sql = "SELECT * FROM Orders WHERE orderid = " + str(id) + ";"
        self.cursor.execute(sql)

        result = self.cursor.fetchone()
        if not result:
            return None
        return OrderObject(result)

    # find reminder by id
    def searchReminderByID(self, id):
        sql = "SELECT * FROM Reminders WHERE reminderid = ?;"
        self.cursor.execute(sql, [(id)])

        result = self.cursor.fetchone()
        if not result:
            return None
        return ReminderObject(result)

    ############################
    ###   UPDATE FUNCTIONS   ###
    ############################

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
    
    ###########################################
    ###   SEARCH BY FOREIGN KEY FUNCTIONS   ###
    ###########################################
    
    def searchOrdersForCustomer(self, id):
        sql = "SELECT * FROM Orders WHERE customerid = ?;"
        self.cursor.execute(sql, [(id)])
        return [OrderObject(o) for o in self.cursor.fetchall() if o != None]
    
    # finds any reminders that pertain to a certian order
    def searchRemindersForOrder(self, id):
        sql = "SELECT * FROM Reminders WHERE orderid = " + str(id) + " LIMIT 1;"
        self.cursor.execute(sql)

        result = self.cursor.fetchone()
        if not result:
            return None
        return ReminderObject(result)