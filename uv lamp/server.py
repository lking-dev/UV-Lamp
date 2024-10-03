from flask import *
import DBAccess
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "dhladhadahldhaldhaldhaldhaldhaldhaldhaldhalhdalhlhadlhaldhaldhaldhl"
database_path = os.path.dirname(os.path.realpath(__file__)) + "\orders.db"

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
    return redirect(url_for("login"))
    
@app.get("/login")
def login_page():
    return render_template("web/login.html", failed = False)

@app.post("/login")
def login():
    userid = try_login(request.form["form-fname"], request.form["form-lname"], request.form["form-email"])

    if not userid:
        return render_template("web/login.html", failed = True)
    else:
        session["username"] = request.form["form-fname"] + " " + request.form["form-lname"]
        session["userid"] = userid

        database = DBAccess.DBAccess(database_path)
        

        return redirect(url_for("user_orders"))

@app.get("/logout")
def logout():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        session.clear()
        return redirect(url_for("login"))
    
@app.get("/user_orders")
def user_orders():
    if "username" not in session:
        return "You are not logged in! <br><a href = '/login'>" + "click here to log in</a>"

    database = DBAccess.DBAccess(database_path)
    orders = database.searchOrdersForCustomer(session["userid"])
    
    return render_template("web/orders.html", orders = orders, username = session["username"])

@app.post("/user_orders/update/<orderid>")
def update_user_order(orderid):
    print("REQUEST TO UPDATE ORDER {} TO RE-INSTALLED".format(orderid))
    orderid = int(orderid)

    database = DBAccess.DBAccess(database_path)
    order = database.searchOrderByID(orderid)

    order.status = 0
    order.lastchanged = datetime.strftime(datetime.now(), "%m/%d/%Y")
    database.updateOrder(order)

    return redirect(url_for("user_orders"))

@app.get("/customer_table")
def customer_table():
    database = DBAccess.DBAccess(database_path)
    rows = database.getAllCustomers()

    return render_template(
        "web/table.html",
        columns = columns_customers,
        rows = rows,
        type = "customer"
    )


@app.get("/order_table")
def order_table():
    database = DBAccess.DBAccess(database_path)
    rows = database.getAllOrders()

    return render_template(
        "web/table.html",
        columns = columns_order,
        rows = rows,
        type = "order"
    )

@app.get("/reminder_table")
def reminder_table():
    database = DBAccess.DBAccess(database_path)
    rows = database.getAllReminders()

    return render_template(
        "web/table.html",
        columns = columns_reminders,
        rows = rows,
        type = "reminder"
    )

def try_login(firstname, lastname, email):
    print("LOGIN ATTEMPT FROM {} {} ({})".format(firstname, lastname, email))
    
    database = DBAccess.DBAccess(database_path)
    user = database.searchCustomerByFields(firstname, lastname, email)

    if user is None:
        return None
    return user.id

app.run()