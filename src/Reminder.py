import sqlite3
import os
import os.path
from datetime import datetime
from pathlib import Path

from Data import Data
from container import customer
from container import order
from container import reminder

# ReminderEngine: handles core functionality for orders and reminders
class Reminder:
    # constructor
    def __init__(self, connector, log_file):
        self.database = connector
        self.log_file = log_file
    
    def printlog(self, log_file, msg):
        fmt_msg = datetime.now().strftime("[%I:%M]") + " " + "[{}]".format(Path(__file__).name) + " " + msg
        print(fmt_msg)
        log_file.write(fmt_msg + "\n")
    
    # core logic for reminder system
    # returns a python list of tuples of customer objects to related order objects
    # ex: [
    #   (Customer1, Order1),
    #   (Customer2, Order2)
    # ]
    # LOGIC IS SPLIT INTO 2 SECTIONS TO MAKE SURE EVERYTHING IS COVERED IN ONE FUNCTION CALL

    # STATUS TABLE:
    # -1: DELETED
    #  0: ALL GOOD
    #  1: IN PROCESS
    #  2: NEEDS REPLACEMENT

    def updateReminders(self):
        # fetch the order data
        data = self.database.getAllOrders()
        relevant = [order for order in data if order.status != -1]
        output = []

        # FIRST RUN: MAKES SURE EVERYTHING HAS AN APPROPRIATE ORDER

        self.printlog(self.log_file, "BEGINNING SEARCHING")

        for order in relevant:
            reminder = self.database.searchRemindersForOrder(order.id)
            customer = self.database.searchCustomerByID(order.customerid)

            if reminder is None:
                self.printlog(self.log_file, "Order " + order.formattedid + " (Placed by " + customer.fullname + ") does not have a reminder! Scheduling one.")
                self.scheduleReminder(order)
            else:
                self.printlog(self.log_file, "Order " + order.formattedid + " (Placed by " + customer.fullname + ") has a reminder scheduled.")

        self.printlog(self.log_file, "END SEARCHING")

        data = self.database.getAllOrders()
        relevant = [order for order in data if order.status != -1]

        self.printlog(self.log_file, "BEGINNING FLAGGING")

        for order in relevant:
            reminder = self.database.searchRemindersForOrder(order.id)
            due = self.testReminder(order, reminder)
            if due:
                order.status = 2
                self.printlog(self.log_file, "Flagged Order #" + order.formattedid + " as NEEDS MAINTENCE")
            else:
                if order.status != 0:
                    self.printlog(self.log_file, "Flagged Order #" + order.formattedid + " as ALL GOOD")
                self.printlog(self.log_file, "Order #" + order.formattedid + " needs no updates, skipping.")

            self.database.updateOrder(order)

        self.printlog(self.log_file, "END FLAGGING")

        self.database.forceCommit()


    # determines the rout of action to be taken on a reminder
    def testReminder(self, order, reminder):
        # grab the current date for comparison
        present = datetime.now()
        # get a datetime object from the string stored in the reminder
        due = datetime.strptime(reminder.date, "%m/%d/%Y")

        # if the date has been passed then send email
        if present >= due:
            return True
        # otherwise no action
        else:
            return False

    # schedules a reminder for an order
    def scheduleReminder(self, order):
        # parse datetime out of last changed text field
        last_change = datetime.strptime(order.lastchanged, "%m/%d/%Y")
        # calculate the due date of the reminder by adding 3 years 
        next_change = last_change.replace(year = last_change.year + 3)
        # convert the new datetime back into a string for the sqlite
        next_date = datetime.strftime(next_change, "%m/%d/%Y")

        # insert the new reminder into the database, linking it to the order
        self.database.addReminder(order.id, next_date)