import sqlite3
import smtplib

import DBConnector
import ReminderEngine

# create the debug database
database = DBConnector.DBConnector()

# add a customer and make a order for him
database.addCustomer("John Doe", "johnd@gmail.com")
id = database.searchCustomerId("John Doe", "johnd@gmail.com")
database.addOrder(id, "09/05/2024")

# create a reminder engine instance to manage the debug database
engine = ReminderEngine.ReminderEngine(database)

# test if any reminders; should say no orders found and make a new one
print("first time:")
engine.handleReminders()

# test for newly created reminder; shoul say reminder found and scheduled in 3 yeasrs time
print("second time:")
engine.handleReminders()