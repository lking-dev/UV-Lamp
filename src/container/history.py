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