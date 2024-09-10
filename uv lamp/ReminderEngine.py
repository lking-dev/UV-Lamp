import sqlite3
import os
import os.path
from datetime import datetime

from DBAccess import DBAccess
from container import customer
from container import order
from container import reminder

# ReminderEngine: handles core functionality for orders and reminders
class ReminderEngine:
    # constructor
    def __init__(self, connector):
        self.database = connector
    
    # goes through all orders and takes action depending on the orders reminders
    def handleReminders(self):
        # fetch the order data
        data = self.database.getAllOrders()
        customers = []

        for order in data:
            # try and get the assoociated reminder for the order
            reminder = self.database.getReminderFromOrder(order.id)

            # if there is a reminder, check if action needs to be taken
            if reminder:
                # index of 1 refers to the scheduled date of the reminder (reminderdate)
                if self.testReminder(order, reminder):
                    customer = self.database.getCustomer(order.customerid)
                    customers.append(customer)

            # if no reminder, schedule a new one
            else:
                self.scheduleReminder(order)
        
        return customers

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

        print("[DEBUG] Scheduled reminder on {} for order {}".format(next_date, order.id))