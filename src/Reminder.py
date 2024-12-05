# Written by Landry M. King, 2024
# Reminder: responsible for scheduling and sending out reminders for contractor orders

import sqlite3
import os
import os.path

from datetime import datetime
from pathlib import Path
from Data import Data

from container.order import OrderObject
from container.history import HistoryEvent
from container.location import LocationObject
from container.customer import CustomerObject
from container.reminder import ReminderObject

class Reminder:
    # constructor
    def __init__(self, connector, log_file):
        self.database = connector
        self.log_file = log_file
    
    def updateReminders(self):
        # fetch the order data
        data = self.database.getAllOrders()
        relevant = [order for order in data if order.status != -1]
        output = []

        # FIRST RUN: MAKES SURE EVERYTHING HAS AN APPROPRIATE ORDER

        for order in relevant:
            reminder = self.database.searchRemindersForOrder(order.id)
            customer = self.database.searchCustomerByID(order.customerid)

            if reminder is None:
                self.scheduleReminder(order)

        data = self.database.getAllOrders()
        relevant = [order for order in data if order.status != -1]


        for order in relevant:
            reminder = self.database.searchRemindersForOrder(order.id)
            due = self.testReminder(reminder)
            if due:
                order.status = 3

            soon = self.testSoonReminder(reminder)
            if soon:
                order.status = 2


            self.database.updateOrder(order)

        self.database.forceCommit()


    # determines the rout of action to be taken on a reminder
    def testReminder(self, reminder):
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
    
    # determines if maintence is due within 3 months time
    def testSoonReminder(self, reminder):
        # grab the current date for comparison
        present = datetime.now()
        # get a datetime object from the string stored in the reminder
        due = datetime.strptime(reminder.date, "%m/%d/%Y")

        days = (present - due).days

        if days <= 90:
            return True
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

if __name__ == "__main__":
    pass