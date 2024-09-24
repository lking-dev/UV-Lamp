from flask import *
import DBAccess
from datetime import datetime

app = Flask(__name__)
app.secret_key = "adhjjaljdal;djhwajw23jdjaw;jdakjd;ajkh;io"

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

        database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")
        

        return redirect(url_for("user_orders"))
    
@app.get("/user_orders")
def user_orders():
    if "username" not in session:
        return "You are not logged in! <br><a href = '/login'>" + "click here to log in</a>"

    database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")
    orders = database.searchOrdersByCustomer(session["userid"])
    
    return render_template("web/orders.html", orders = orders)

@app.post("/user_orders/update/<orderid>")
def update_user_order(orderid):
    print("REQUEST TO UPDATE ORDER {} TO RE-INSTALLED".format(orderid))
    orderid = int(orderid)

    database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")
    order = database.searchOrderById(orderid)

    if order.status == 0: order.status = 1
    elif order.status == 1: order.status = 0
    order.lastchanged = datetime.strftime(datetime.now(), "%m/%d/%Y")
    database.updateOrder(order)

    return redirect(url_for("user_orders"))

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

def try_login(firstname, lastname, email):
    print("LOGIN ATTEMPT FROM {} {} ({})".format(firstname, lastname, email))
    
    database = DBAccess.DBAccess(r"C:\Users\lking\Desktop\UV-Lamp\uv lamp\orders.db")
    id = database.searchForCustomerId(firstname, lastname, email)

    if id is None:
        return None
    return id

app.run()