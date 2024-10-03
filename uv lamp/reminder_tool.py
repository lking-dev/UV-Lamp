import sqlite3
import smtplib
import os
import json

from datetime import datetime
from Data import Data
from Emailer import Emailer
from Reminder import Reminder

path = os.path.dirname(os.path.realpath(__file__))

def printlog(log_file, msg):
    log_file.write(datetime.now().strftime("[%X] ") + msg + "\n")

def main():
    config_file = open(path + "\\config\\reminders.json", "r")
    config = json.load(config_file)
    config_file.close()

    global log_file
    log_file = open(path + config["log_directory"] + datetime.now().strftime("log-%I-%M-%B-%d-%Y") + ".txt", "w")

    database = Data(config["database"])
    reminder = Reminder(database, log_file)
    printlog(log_file, "Connected to database at {}".format(config["database"]))
    emailclient = Emailer(config["sender"], config["api"])
    printlog(log_file, "Sendgrid email client initialized")
    printlog(log_file, "Searching for unscheduled reminders")

    customers = reminder.getReminders()
    print(customers)

    log_file.close()
        
if __name__ == "__main__":
    main()