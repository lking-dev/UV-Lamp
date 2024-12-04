from flask import *
from Data import Data
from datetime import datetime
from container import order
from container.order import OrderObject
from container.history import HistoryEvent
from container.location import LocationObject
from container.customer import CustomerObject
from PGData import PGData
import GoogleMapsAPI
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
   

# TODO: ADD ERROR MESSAGES/HANDLING FOR INVALID ADDRESSES
# USE GOOGLE MAPS ADDRESS VALIDATION API
@app.post("/pages/signup")
def signup():
    database = Data(database_path)

    address_components = [request.form["form-address{}".format(i)] for i in range(4)]
    final_location = -1

    # entering an address is OPTIONAL for the contractor
    # this function validates that an actual address was entered
    # otherwise its assumed they didnt enter one
    if validate_address(*address_components):
        latlong = GoogleMapsAPI.geolocateAddress("{}, {}, {} {}".format(*address_components))
        possible_location = database.searchLocationByCoordinates(*latlong)

        if possible_location is None:
            locationid = database.addLocation(*address_components, latlong[0], latlong[1])
            final_location = locationid
        else:
            final_location = possible_location.id  

    database.addCustomer(
        request.form["form-firstname"],
        request.form["form-lastname"],
        request.form["form-email"],
        request.form["form-company"],
        request.form["form-password"],
        final_location)      
    
    return render_template("web/login.html")



# user orders page, the heart of the website, displays all the orders that the user has 
@app.get("/pages/orders")
def user_orders():
    database = Data(database_path)

    orders = database.searchOrdersForCustomer(session["userid"]) # HARDCODED FOR DEBUG
    reminders = [database.searchRemindersForOrder(order.id) for order in orders]
    locations = [database.searchLocationByID(order.locationid) for order in orders]
    # LATITUDE AND LONGITUDE HAVE TO BE SWITCHED FOR THE API CALL
    # IDK WHAT I DID BUT IT MUST BE SWITCHED TO WORK
    streetviewlinks = [GoogleMapsAPI.constructStreetviewRequest((location.longitude, location.latitude), (480, 640), 60) for location in locations]
    locationlinks = [GoogleMapsAPI.constructMapsURL(location) for location in locations]
    
    return render_template("web/orders_template.html",
        orders = orders,
        reminders = reminders,
        locations = locations,
        streetviewlinks = streetviewlinks,
        locationlinks = locationlinks)


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

    # the SKU's of the items stored here follow the following format:
    # TUVL-<year: 1 digit><size (inch): 2 digits)><pig-tail (OPTIONAL): 1 character ('P')>"
    # so the SKU's warranty can be extracted from the 6th character of the SKU (index 5)
    productwarranty = product["sku"][5] + " Year"
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



@app.get("/pages/register")
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
    database.addHistory()
    
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
    orderid = database.addOrder(new)

    history_msg = HistoryEvent.eventMsg["creation"]
    database.addHistory(get_current_date(), history_msg, orderid)

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

def validate_address(address, city, state, zipcode):
    components = [address, city, state, zipcode]
    for component in components:
        if component == None or component == "":
            return False
    return True

# try login: determines a login requests validity
def try_login(email, password):
    print("LOGIN ATTEMPT FROM {} WITH LOGIN {}".format(email, password))
    
    database = Data(database_path)
    userid = database.customerLoginSearch(email, password)

    if userid is None:
        return None
    return userid

def get_current_date():
    now = datetime.now()
    date = datetime.strptime(now, "%m/%d/%Y")
    return date

# method for rearranging orders to display the active orders first, then the deleted orders
def rearrange_orders(orders):
    active = [o for o in orders if o.status != 2]
    inactive = [o for o in orders if o.status == 2]
    return active + inactive

# main method that sets up and runs the server
def main():
    app.run(host = "10.10.101.226", port=80)

if __name__ == "__main__":
    main()