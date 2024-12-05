import sqlite3
import os
import json
from pathlib import Path

from datetime import datetime
from Data import Data
from Emailer import Emailer
from Reminder import Reminder

path = os.path.dirname(os.path.realpath(__file__))

def main():
    config_file = open(path + "\\config\\reminders.json", "r")
    config = json.load(config_file)
    config_file.close()

    database = Data(path + "\\" + config["database"])
    
    reminder = Reminder(database, None)
    reminders = reminder.updateReminders()

    emailclient = Emailer(email = config["sender"], key = config["api"])
    return
    for customer in reminders:
        try:
            emailclient.sendEmail(
                "lanmanking@yahoo.com",
                "Replacement for UV Lamp Filter",
                config["template"],
                {"fullname": customer.firstname + " " + customer.lastname}
            )
            printlog(log_file, "Send email to " + customer.email)
        except:
            printlog(log_file, "Failed to send email to " + customer.email)

    printlog(log_file, "Finished.")
        
if __name__ == "__main__":
    main()