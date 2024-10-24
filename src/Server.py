from flask import *
from Data import Data
from datetime import datetime
from container import order
from container.order import OrderObject
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

#################
### WEB PAGES ###
#################

# the home page, redirects any default requests to the login page
@app.route("/")
def index():
    return redirect("/pages/login")

# the actual login page, for GET requests 
@app.get("/pages/login") 
def login_page():
    return render_template("web/login.html", failed = False)

# login page logic using POST form
# either sends user to their orders or redirects to the login page with an error message
@app.post("/pages/login")
def login():
    userid = try_login(request.form["form-fname"], request.form["form-lname"], request.form["form-email"])

    if not userid:
        return render_template("web/login.html", failed = True)
    else:
        session["username"] = request.form["form-fname"] + " " + request.form["form-lname"]
        session["userid"] = userid

        database = Data(database_path)

        return redirect("/pages/orders")
    
# logout page, just clears the session then re-routs to login page
@app.get("/pages/logout")
def logout():
    if "username" not in session:
        return redirect("/pages/login")
    else:
        session.clear()
        return redirect("/pages/login")
    
# user orders page, the heart of the website, displays all the orders that the user has 
@app.get("/pages/orders")
def user_orders():
    if "username" not in session:
        return "You are not logged in! <br><a href = '/login'>" + "click here to log in</a>"

    database = Data(database_path)
    orders = database.searchOrdersForCustomer(session["userid"])
    orders = rearrange_orders(orders)
    
    return render_template("web/orders.html", orders = orders, username = session["username"])

@app.get("/pages/register_order")
def register_order():
    return render_template("web/register.html")

# updates an orders status using POST and url arguments
@app.get("/pages/update_order/<orderid>")
def update_order_page(orderid):
    database = Data(database_path)
    order = database.searchOrderByID(orderid)

    return render_template("web/update.html", order = order)

##################
### ORDERS API ###
##################

@app.post("/api/order/<orderid>/update")
def update_order(orderid):
    database = Data(database_path)
    order = database.searchOrderByID(orderid)

    order.placed = request.form["form-placed"]
    order.lastchanged = request.form["form-last"]
    order.location = request.form["form-location"]
    order.status = 1

    database.updateOrder(order)
    
    reminder = database.searchRemindersForOrder(order.id)
    if reminder:
        database.delReminder(reminder)

    return redirect("/pages/orders")

# deletes an order using POST
@app.get("/api/order/<orderid>/delete")
def delete_order(orderid):
    print("REQUEST TO DELETE ORDER {}".format(orderid))
    orderid = int(orderid)

    database = Data(database_path)
    order = database.searchOrderByID(orderid)

    order.status = -1
    database.updateOrder(order)

    return redirect("/pages/orders")

# creates an order using POST form
@app.post("/api/order/create")
def create_order():
    print("REQUEST TO CREATE ORDER")

    new = OrderObject()
    new.placed = request.form["form-placed"]
    new.lastchanged = request.form["form-lastchanged"]
    new.customerid = session["userid"]
    new.location = request.form["form-location"]
    new.status = 1

    database = Data(database_path)
    database.addOrder(new)

    return redirect("/pages/orders")

###################
### ADMIN PAGES ###
###################

# admin page, views all the rows in the customer table
@app.get("/pages/admin/customer_table")
def customer_table():
    database = Data(database_path)
    rows = database.getAllCustomers()

    return render_template(
        "web/table.html",
        columns = columns_customers,
        rows = rows,
        type = "customer"
    )

# admin page, views all the rows in the orders table
@app.get("/pages/admin/order_table")
def order_table():
    database = Data(database_path)
    rows = database.getAllOrders()

    return render_template(
        "web/table.html",
        columns = columns_order,
        rows = rows,
        type = "order"
    )

# admin page, views all the rows in the reminder table
@app.get("/pages/admin/reminder_table")
def reminder_table():
    database = Data(database_path)
    rows = database.getAllReminders()

    return render_template(
        "web/table.html",
        columns = columns_reminders,
        rows = rows,
        type = "reminder"
    )

#########################
### NON WEB FUNCTIONS ###
#########################

# try login: determines a login requests validity
def try_login(firstname, lastname, email):
    print("LOGIN ATTEMPT FROM {} {} ({})".format(firstname, lastname, email))
    
    database = Data(database_path)
    user = database.searchCustomerByFields(firstname, lastname, email)

    if user is None:
        return None
    return user.id

# method for rearranging orders to display the active orders first, then the deleted orders
def rearrange_orders(orders):
    active = [o for o in orders if o.status != 2]
    inactive = [o for o in orders if o.status == 2]
    return active + inactive

# main method that sets up and runs the server
def main():
    app.run(host = "10.10.101.221", port=80)

if __name__ == "__main__":
    main()