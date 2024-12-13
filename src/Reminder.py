# Written by Landry M. King, 2024
# Reminder: responsible for scheduling and sending out reminders for contractor orders

import sqlite3
import os
import os.path

from datetime import datetime
from datetime import timedelta
from pathlib import Path

from Data import Data
from Config import Config
from Emailer import Emailer

from container.order import OrderObject
from container.history import HistoryEvent
from container.customer import CustomerObject
from container.reminder import ReminderObject


def manage_reminders(database: Data):
    print("Starting manage_reminders()")
    orders = database.getAllOrders()
    scheduled = []

    for order in orders:
        print("Checking order {}".format(order.id))

        last_changed = datetime.strptime(order.lastchanged, "%m/%d/%Y")
        warranty_days = order.warranty * 365
        due_date = last_changed + timedelta(days = warranty_days)
        current_date = datetime.now()

        print("Order {} is due for change on {}".format(order.id, due_date))

        reminder = database.searchRemindersForOrder(order.id)
        if not reminder:
            print("Order {} does not have a reminder scheduled, fixing".format(order.id))
            due_string = datetime.strftime(due_date, "%m/%d/%Y")
            database.addReminder(order.id, due_string)
            database.addHistory(getCurrentDate(), "Scheduled Reminder for {}".format(due_string), order.id)
        else:
            print("Reminder found for order {}".format(order.id))

        previous_status = order.status

        # order is past due
        if current_date > due_date:
            order.status = 3
            if previous_status != 3:
                database.addHistory(getCurrentDate(), "Status set to \"Needs Maintence\"", order.id)
            scheduled.append(order)
            print("Order {} is due for maintence".format(order.id))
        # order change within 90 days
        elif (due_date - current_date).days < 90:
            order.status = 2
            if previous_status != 2:
                database.addHistory(getCurrentDate(), "Status set to \"Due Soon\"", order.id)
            print("Order {} is due for maintence in 90 days".format(order.id))
        # else: all good!
        else:
            order.status = 0
            if previous_status != 0:
                database.addHistory(getCurrentDate(), "Status set to \"All Good\"", order.id)
            print("Order {} is up to date".format(order.id))

        database.updateOrder(order)
        print()

    print("Ending manage_reminders()")
    print("Found {} past due orders\n".format(len(scheduled)))
    return scheduled

def send_reminders(scheduled, database: Data, emailClient: Emailer):
    print("Starting send_reminders()")
    for order in scheduled:
        contractor = database.searchCustomerByID(order.customerid)

        emailClient.sendEmail(
            contractor.email,
            "UV-Lamp Replacement Needed",
            Config().getEmailTemplate(),
            {"order": order, "customer": contractor, "host": Config().getHost()}
        )

        print("Sent Email to {} ({})".format(contractor.fullname, contractor.email))
    
    print("Ending send_reminders()")

def getCurrentDate():
    now = datetime.now()
    date = datetime.strftime(now, "%m/%d/%Y")
    return date

def main():
    configuration = Config()
    database_path = configuration.getDatabasePath()
    database_connection = Data(database_path)

    (email, api_key) = configuration.getSendgridCreds()
    email_client = Emailer(email, api_key)

    print("(Reminder.py): Starting processing")

    scheduled = manage_reminders(database_connection)
    send_reminders(scheduled, database_connection, email_client)

    print("Finished processing orders.")

if __name__ == "__main__":
    main()