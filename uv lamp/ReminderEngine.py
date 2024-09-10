import sqlite3
import os
import os.path
from datetime import datetime

from DBAccess import DBAccess
from Container import CustomerObject
from Container import ReminderObject
from Container import OrderObject

# ReminderEngine: handles core functionality for orders and reminders
class ReminderEngine:
    # constructor
    def __init__(self, connector):
        self.database = connector
    
    # goes through all orders and takes action depending on the orders reminders
    def handleReminders(self):
        # fetch the order data
        data = self.database.getAllOrders()

        for order in data:
            # try and get the assoociated reminder for the order
            reminder = self.database.getReminderFromOrder(order.id)

            # if there is a reminder, check if action needs to be taken
            if reminder:
                # index of 1 refers to the scheduled date of the reminder (reminderdate)
                print("[DEBUG] Reminder found for order {}, scheduled on {}".format(order.id, reminder.date))
                self.executeReminder(order, reminder)

            # if no reminder, schedule a new one
            else:
                print("[DEBUG] No reminders found for order {}".format(order.id))
                self.scheduleReminder(order)

    # determines the rout of action to be taken on a reminder
    def executeReminder(self, order, reminder):
        # grab the current date for comparison
        present = datetime.now()
        # get a datetime object from the string stored in the reminder
        due = datetime.strptime(reminder.date, "%m/%d/%Y")

        # if the date has been passed then send email
        if present >= due:
            print("[DEBUG] Reminder email needed for order {}".format(order.id))
        # otherwise no action
        else:
            print("[DEBUG] Reminder action not needed for order {}".format(order.id))

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