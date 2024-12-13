import os
from flask import *
from datetime import datetime

from Data import Data
from Config import Config
#from PGData import PGData
import Maps

from container.order import OrderObject
from container.history import HistoryEvent
from container.customer import CustomerObject
from container.reminder import ReminderObject

app = Flask(__name__)
app.secret_key = "nclhezsioehfljenjzsbkljczosieliblh"
configuration = Config()
database_path = configuration.getDatabasePath()

# the home page, redirects any default requests to the login page
@app.route("/")
def index():
    return redirect("/pages/login")

# the actual login page, for GET requests 
@app.get("/pages/login") 
def login_page():
    session.clear()
    return render_template("web/login.html", failed = False)

# login page logic using POST form
# either sends user to their orders or redirects to the login page with an error message
@app.post("/pages/login")
def login():
    userid = try_login(request.form["form-email"], request.form["form-password"])

    if not userid:
        return render_template("web/login.html", failed = True)
    else:
        session["userid"] = userid
        return redirect("/pages/orders/user/{}".format(userid))
    
# logout page, just clears the session then re-routs to login page
@app.get("/pages/logout")
def logout():
    session.clear()
    return redirect("/pages/login")

@app.get("/pages/signup")
def signup_page():
    return render_template("web/signup.html")
   
@app.post("/pages/signup")
def signup():
    database = Data(database_path)

    database.addCustomer(
        firstname = request.form["form-firstname"],
        lastname = request.form["form-lastname"],
        company = request.form["form-company"],
        email = request.form["form-email"],
        password = request.form["form-password"],
    )
    
    return render_template("web/login.html")

# user orders page, the heart of the website, displays all the orders that the user has 
@app.get("/pages/orders/user/<userid>")
def user_orders(userid):
    database = Data(database_path)

    orders = database.searchOrdersForCustomer(userid)

    if len(orders) < 1:
        return render_template("web/orders_template.html", anyorders = False)

    reminders = [database.searchRemindersForOrder(order.id) for order in orders]
    
    return render_template("web/orders_template.html",
        anyorders = True,
        orders = orders,
        reminders = reminders)

# kind of unessecary, but useful for shortening urls
# pulls up the offical page for a particular diversitech product
@app.get("/pages/items/view/<sku>")
def view_item(sku):
    return redirect(f"https://www.diversitech.com/product/search?keyword={sku}")

@app.get("/pages/items/view")
def view_items():
    return redirect("https://www.diversitech.com/product-families/indoor-air-quality/residential-indoor-air-quality/replacement-uv-lamps")

# the heart of this app. anything important you want to know is here
@app.get("/pages/orders/<orderid>")
def more_info_page(orderid):
    if "userid" not in session:
        return "You are not logged in! <br><a href = '/pages/login'>" + "click here to log in</a>"

    # get the local sqlite3 connection
    database = Data(database_path)
    # get the external connection to ORO UAT5
    #orodb = PGData()
    
    # grab all relevant data to be shipped to template
    order = database.searchOrderByID(orderid)
    customer = database.searchCustomerByID(order.customerid)
    history = database.searchHistoryForOrder(orderid)

    daysuntildue = None
    reminder = None

    if order.status != 1:
        reminder = database.searchRemindersForOrder(order.id)

        diff = (datetime.strptime(reminder.date, "%m/%d/%Y") - datetime.now()).days
        if diff <= 0: daysuntildue = "Past Due"
        else: daysuntildue = str(diff) + " Days"

    #product = orodb.getProductData(order.sku)

    # return the template formatted with the given information
    return render_template("web/info_template.html",
        order = order,
        customer = customer,
        history = history,
        reminder = reminder,
        daysuntildue = daysuntildue,
        product = None,
        productwarranty = order.getWarranty())

# page for registering new orders
@app.get("/pages/register")
def register_page():
    return render_template("web/register.html")

@app.post("/pages/register")
def register_order():
    database = Data(database_path)

    address = "{}, {}, {} {}".format(
        request.form["form-address0"],
        request.form["form-address1"],
        request.form["form-address2"],
        request.form["form-address3"])
    
    validated_address = Maps.validateAddress(address)
    (lat, long) = Maps.geolocateAddress(validated_address)
    warranty = int(request.form["form-itemid"][5])

    database.addOrder(
        placed = request.form["form-placeddate"],
        last = request.form["form-lastdate"],
        status = 1, # IN PROCESS STATUS
        address = validated_address,
        latitude = lat,
        longitude = long,
        original = request.form["form-originaldate"],
        sku = request.form["form-itemid"],
        customerid = session["userid"],
        warranty = warranty,
        homephone = request.form["form-homephone"]
    )

    return redirect("/pages/orders/user/{}".format(session["userid"]))

# updates an orders status using POST and url arguments
@app.get("/pages/update/<orderid>")
def update_order_page(orderid):
    database = Data(database_path)
    order = database.searchOrderByID(orderid)

    return render_template("web/update.html", order = order)

@app.post("/pages/update/<orderid>")
def update_order(orderid):
    database = Data(database_path)
    order = database.searchOrderByID(orderid)

    order.status = 1 # SET STATUS TO IN PROCESS
    order.lastchanged = request.form["form-changedate"]
    database.updateOrder(order)

    current_reminder = database.searchRemindersForOrder(order.id)

    if current_reminder:
        database.delReminder(current_reminder)

    change_type = request.form["form-wasmaintence"].upper()

    if change_type == "YES":
        database.addHistory(get_current_date(), "Order Updated (Emergency)", order.id)
    else:
        database.addHistory(get_current_date(), "Order Updated (Regular)", order.id)

    return redirect("/pages/orders/user/{}".format(session["userid"]))

# deletes an order
@app.get("/api/order/<orderid>/delete")
def delete_order(orderid):
    orderid = int(orderid)

    database = Data(database_path)
    order = database.searchOrderByID(orderid)

    if order:
        database.delOrder(order)

    return redirect("/pages/orders")

# try login: determines a login requests validity
def try_login(email, password):    
    database = Data(database_path)
    userid = database.customerLoginSearch(email, password)

    if userid is None:
        return None
    return userid

def get_current_date():
    now = datetime.now()
    date = datetime.strftime(now, "%m/%d/%Y")
    return date

# method for rearranging orders to display orders in decreasing priority
# e.g. orders that need replacement show up first
def rearrange_orders(orders):
    urgent = [o for o in orders if o.status == 3]
    soon = [o for o in orders if o.status == 2]
    good = [o for o in orders if o.status == 1]
    inprocess = [o for o in orders if o.status == 0]
    return urgent + soon + good + inprocess

# main method that sets up and runs the server
def main():
    app.run(host = configuration.getHost(), port = configuration.getPort())

if __name__ == "__main__":
    main()