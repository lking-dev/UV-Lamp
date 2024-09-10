# generic reminder object for holding data in named fields instead of a set

# REMINDERS SCHEMA:
# reminderid INTEGER PRIMARY KEY AUTOINCREMENT
# reminderdate TEXT
# orderid INTEGER (FOREIGN KEY)

class ReminderObject:
    def __init__(self, data):
        self.id = data[0]
        self.date = data[1]
        self.orderid = data[2]