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
        fmt_msg = datetime.now().strftime("[%X]") + " " + "[{}]".format(Path(__file__).name) + " " + msg
        print(fmt_msg)
        log_file.write(fmt_msg + "\n")

    def repeatCustomer(self, customers, test):
        for customer in customers:
            if customer.id == test.id:
                return True
            
        return False
    
    # goes through all orders and takes action depending on the orders reminders
    def getReminders(self):
        # fetch the order data
        data = self.database.getAllOrders()
        customers = []

        needed_reminder = 0
        needed_scheduling = 0
        needed_nothing = 0

        self.printlog(self.log_file, "Handling Reminders...")
        
        for order in data:
            # try and get the assoociated reminder for the order
            reminder = self.database.searchRemindersForOrder(order.id)

            # if there is a reminder, check if action needs to be taken
            if reminder:
                if self.testReminder(order, reminder):
                    customer = self.database.searchCustomerByID(order.customerid)
                    
                    copy = order;
                    copy.status = 0
                    self.database.updateOrder(copy)
                    
                    if customer not in customers:
                        customers.append(customer)

                    needed_reminder += 1
                else:
                    self.database.updateOrder(order)
                    needed_nothing += 1
            # if no reminder, schedule a new one
            else:
                self.scheduleReminder(order)
                needed_scheduling += 1

        self.printlog(self.log_file, "Finished.")
        self.printlog(self.log_file, "Found {} Unscheduled Orders".format(needed_scheduling))
        self.printlog(self.log_file, "Found {} Overdue Orders".format(needed_reminder))
        self.printlog(self.log_file, "Found {} Compliant Orders".format(needed_nothing))
        self.printlog(self.log_file, "Searched {} Orders Total".format(len(data)))
        
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