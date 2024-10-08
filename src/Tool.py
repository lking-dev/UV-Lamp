import sqlite3
import smtplib
import os
import json
from pathlib import Path

from datetime import datetime
from Data import Data
from Emailer import Emailer
from Reminder import Reminder

path = os.path.dirname(os.path.realpath(__file__))

def printlog(log_file, msg):
    fmt_msg = datetime.now().strftime("[%X]") + " " + "[{}]".format(Path(__file__).name) + " " + msg
    print(fmt_msg)
    log_file.write(fmt_msg + "\n")

def main():
    config_file = open(path + "\\config\\reminders.json", "r")
    config = json.load(config_file)
    config_file.close()

    global log_file
    log_file = open(path + config["log_directory"] + datetime.now().strftime("log-%I-%M-%B-%d-%Y") + ".txt", "w")

    database = Data(path + "\\" + config["database"])
    printlog(log_file, "Connected to database \"{}\"".format(config["database"]))
    
    reminder = Reminder(database, log_file)
    printlog(log_file, "Searching for unscheduled reminders")
    reminders = reminder.getReminders()

    emailclient = Emailer(email = config["sender"], key = config["api"], log_file = log_file)
    printlog(log_file, "Sendgrid email client initialized")

    for customer in reminders:
        try:
            emailclient.sendEmail(
                "lanmanking@yahoo.com",
                "Replacement for UV Lamp Filter",
                config["template"],
                {"fullname": customer.firstname + " " + customer.lastname}
            )
        except:
            print("Email to " + customer.email + " failed")

    log_file.close()
        
if __name__ == "__main__":
    main()