# generic reminder object for holding data in named fields instead of a set

# REMINDERS SCHEMA:
# reminderid INTEGER PRIMARY KEY AUTOINCREMENT
# reminderdate TEXT
# orderid INTEGER (FOREIGN KEY)

import datetime

class ReminderObject:
    def __init__(self, data):
        self.id = data["reminderid"]
        self.date = data["reminderdate"]
        self.orderid = data["orderid"]
        self.formatteddate = self.nicedate()

    def nicedate(self, date):
        placed = datetime.strptime(date, "%m/%d/%Y")

        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dayname = weekdays[placed.weekday()]

        