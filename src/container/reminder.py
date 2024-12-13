# Written by Landry M. King, 2024
# ReminderObject: represents a row of the "Orders" table

from datetime import datetime

class ReminderObject:
    def __init__(self, data):
        self.id = data["reminderid"]
        self.date = data["reminderdate"]
        self.orderid = data["orderid"]
        self.formatteddate = self.nicedate(self.date)

    def nicedate(self, date):
        dt = datetime.strptime(date, "%m/%d/%Y")

        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        endings = {
            "1": "rst", "2": "nd", "3": "rd", "4": "th", "5": "th", "6": "th", "7": "th", "8": "th", "9": "th", "10": "th",
            "11": "th", "12": "th", "13": "th", "14": "th", "15": "th", "16": "th", "17": "th", "18": "th", "19": "th", "20": "th",
            "21": "rst", "22": "nd", "23": "rd", "24": "th", "25": "th", "26": "th", "27": "th", "28": "th", "29": "th", "30": "th",
            "31": "rst"
        }

        nice = weekdays[dt.weekday()] + ", " + months[dt.month - 1] + " " + str(dt.day) + endings[str(dt.day)] + ", " + str(dt.year)
        return nice



        