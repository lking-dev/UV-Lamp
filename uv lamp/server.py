from flask import *
import DBAccess

app = Flask(__name__)

columns_customers = {
    "id": "ID",
    "fname": "Firstname",
    "lname": "Lastname",
    "company": "Company",
    "email": "Email Address",
    "phone": "Phone Number"
}

columns_order = {
    "id": "ID",
    "placed": "Date of Placement",
    "last": "Date Last Changed",
    "customerid": "Linked Customer ID"
}

columns_reminders = {
    "id": "ID",
    "date": "Date Scheduled",
    "orderid": "Linked Order ID"
}

@app.route("/")
def home_page():
    return redirect(url_for("customer_table"))
    

@app.get("/customer_table")
def customer_table():
    database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")
    rows = database.getAllCustomers()

    return render_template(
        "web/table.html",
        columns = columns_customers,
        rows = rows,
        type = "customer"
    )


@app.get("/order_table")
def order_table():
    database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")
    rows = database.getAllOrders()

    return render_template(
        "web/table.html",
        columns = columns_order,
        rows = rows,
        type = "order"
    )

@app.get("/reminder_table")
def reminder_table():
    database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")
    rows = database.getAllReminders()

    return render_template(
        "web/table.html",
        columns = columns_reminders,
        rows = rows,
        type = "reminder"
    )

app.run()