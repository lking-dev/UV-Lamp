import sqlite3
import smtplib
import os

import DBAccess
import ReminderEngine

# create the debug database
database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")

# create a reminder engine instance to manage the debug database
engine = ReminderEngine.ReminderEngine(database)

# test if any reminders; should say no orders found and make a new one
print("first time:")
engine.handleReminders()

# test for newly created reminder; shoul say reminder found and scheduled in 3 yeasrs time
print("second time:")
engine.handleReminders()