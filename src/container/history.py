# generic order object for holding data in named fields instead of a set


# .schema as of 11/26/2024
# CREATE TABLE OrderHistory (
#   historyid INTEGER PRIMARY KEY AUTOINCREMENT,
#   historydate TEXT,
#   linkedorderid INTEGER,
#   historycontent TEXT,
#   FOREIGN KEY(linkedorderid) REFERENCES Orders(orderid)
# );
class HistoryEvent:
    eventMsg = {
        "creation": "Order Created",
        "reminder set": "Reminder Scheduled {}",
        "status change": "Status Set to {}",
        "email sent": "Email Sent"
    }     

    def __init__(self, data):        
        self.id = data["historyid"]
        self.date = data["historydate"]
        self.linkedorder = data["linkedorderid"]
        self.content = data["historycontent"]