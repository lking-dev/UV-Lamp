import os
from flask import *
from datetime import datetime

from Data import Data
from Config import Config
from PGData import PGData
from random import randint
import GoogleMapsAPI

from container.order import OrderObject
from container.history import HistoryEvent
from container.location import LocationObject
from container.customer import CustomerObject
from container.reminder import ReminderObject

app = Flask(__name__)
app.secret_key = "aghdeahdkhadkhakdhakdhakdhakdhakdhakhdakhdakhdakhyd"
configuration = Config()
database_path = configuration.getDatabasePath()

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
    userid = try_login(request.form["form-email"], request.form["form-password"])

    if not userid:
        return render_template("web/login.html", failed = True)
    else:
        session["userid"] = userid

        return redirect("/pages/orders")
    
# logout page, just clears the session then re-routs to login page
@app.get("/pages/logout")
def logout():
    if "username" not in session:
        return redirect("/pages/login")
    else:
        session.clear()
        return redirect("/pages/login")

@app.get("/pages/signup")
def signup_page():
    return render_template("web/signup.html")
   
@app.post("/pages/signup")
def signup():
    database = Data(database_path)

    address = "{}, {}, {} {}".format(
        request.form["form-address0"],
        request.form["form-address1"],
        request.form["form-address2"],
        request.form["form-address3"])
    
    validated_address = GoogleMapsAPI.validateAddress(address)
    locationid = -1

    if validated_address:
        (lat, long) = GoogleMapsAPI.geolocateAddress(validated_address)
        potential = database.searchLocationByCoordinates(lat, long)

        if potential:
            locationid = potential.id
        else:
            locationid = database.addLocation(validated_address, lat, long, "CONTRACTOR_LOCATION")
    
    database.addCustomer(
        request.form["form-firstname"],
        request.form["form-lastname"],
        request.form["form-email"],
        request.form["form-company"],
        request.form["form-password"],
        locationid
    )
    
    return render_template("web/login.html")

# user orders page, the heart of the website, displays all the orders that the user has 
@app.get("/pages/orders")
def user_orders():
    database = Data(database_path)

    orders = database.searchOrdersForCustomer(session["userid"])

    if len(orders) < 1:
        return render_template("web/orders_template.html", anyorders = False)

    reminders = [database.searchRemindersForOrder(order.id) for order in orders]
    locations = [database.searchLocationByID(order.locationid) for order in orders]
    # latitiude and longitude have to be switched
    # this problem occurs in other places throughout the code
    # why? im not sure. but requires them to be reversed to work
    streetviewlinks = [GoogleMapsAPI.constructStreetviewRequest((location.latitude, location.longitude), (480, 640), 60) for location in locations]
    locationlinks = [GoogleMapsAPI.constructMapsURL(location) for location in locations]
    
    return render_template("web/orders_template.html",
        anyorders = True,
        orders = orders,
        reminders = reminders,
        locations = locations,
        streetviewlinks = streetviewlinks,
        locationlinks = locationlinks)

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
    # REMOVED FOR DEBUG
    #if "userid" not in session:
        #return "You are not logged in! <br><a href = '/pages/login'>" + "click here to log in</a>"

    # get the local sqlite3 connection
    database = Data(database_path)
    # get the external connection to ORO UAT5
    orodb = PGData()
    
    # grab all relevant data to be shipped to template
    order = database.searchOrderByID(orderid)
    customer = database.searchCustomerByID(order.customerid)
    history = database.searchHistoryForOrder(orderid)
    location = database.searchLocationByID(order.locationid)
    reminder = database.searchRemindersForOrder(order.id)
    product = orodb.getProductData(order.sku)

    productwarranty = str(order.warranty) + " Year"
    product_sku = product["sku"]
    # if the warranty is greater than a year change the text to "Years" instead of "Year"
    if int(product["sku"][5]) > 1: productwarranty += "s"

    # grab the maps url for a given address
    generatedmapslink = GoogleMapsAPI.constructMapsURL(location)

    # calculate the days until a given order is due
    diff = (datetime.strptime(reminder.date, "%m/%d/%Y") - datetime.now()).days
    daysuntildue = None
    if diff <= 0: daysuntildue = "Past Due"
    else: daysuntildue = str(diff) + " Days"

    # return the template formatted with the given information
    return render_template("web/info_template.html",
        order = order,
        customer = customer,
        history = history,
        location = location,
        reminder = reminder,
        generatedmapslink = generatedmapslink,
        daysuntildue = daysuntildue,
        product = product,
        productwarranty = productwarranty,
        product_sku = product_sku)

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
    
    validated_address = GoogleMapsAPI.validateAddress(address)
    (lat, long) = GoogleMapsAPI.geolocateAddress(validated_address)
    location = database.searchLocationByCoordinates(lat, long)
    locationid = -1

    if location:
        locationid = location.id
    else:
        locationid = database.addLocation(validated_address, lat, long, request.form["form-homephone"])

    database.addOrder(
        request.form["form-placeddate"],
        request.form["form-originaldate"],
        request.form["form-lastdate"],
        session["userid"],
        1, # IN PROCESS!
        locationid,
        request.form["form-itemid"]
    )

    return redirect("/pages/orders")

# updates an orders status using POST and url arguments
@app.get("/pages/update/<orderid>")
def update_order_page(orderid):
    database = Data(database_path)
    order = database.searchOrderByID(orderid)

    return render_template("web/update.html", order = order)

@app.post("/api/order/<orderid>/update")
def update_order(orderid):
    database = Data(database_path)
    order = database.searchOrderByID(orderid)

    order.placed = request.form["form-placed"]
    order.lastchanged = request.form["form-last"]
    order.location = request.form["form-location"]
    order.status = 1

    database.updateOrder(order)
    database.addHistory()
    
    reminder = database.searchRemindersForOrder(order.id)
    if reminder:
        database.delReminder(reminder)

    return redirect("/pages/orders")

# deletes an order
@app.get("/api/order/<orderid>/delete")
def delete_order(orderid):
    orderid = int(orderid)

    database = Data(database_path)
    order = database.searchOrderByID(orderid)
    database.delOrder(order)

    return redirect("/pages/orders")

# creates an order using POST form
@app.post("/api/order/create")
def create_order():
    new = OrderObject()
    new.placed = request.form["form-placed"]
    new.lastchanged = request.form["form-lastchanged"]
    new.customerid = session["userid"]
    new.location = request.form["form-location"]
    new.status = 1

    database = Data(database_path)
    orderid = database.addOrder(new)

    history_msg = HistoryEvent.eventMsg["creation"]
    database.addHistory(get_current_date(), history_msg, orderid)

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
    date = datetime.strptime(now, "%m/%d/%Y")
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