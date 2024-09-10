import sqlite3
import smtplib
import os

import DBAccess
import ReminderEngine
import EmailHandler

# create the debug database
database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")

# create a reminder engine instance to manage the debug database
engine = ReminderEngine.ReminderEngine(database)
emailclient = EmailHandler.EmailHandler("reminder@diversitech.com")

customers = engine.handleReminders()

for customer in customers:
    emailclient.sendEmail(
        customer.email,
        "UV-Lamp Replacement Reminder",
        "C:\\Users\\lking\\Desktop\\UV-Lamp\\uv lamp\\templates\\",
        "test.html",
        {"name": customer.firstname})