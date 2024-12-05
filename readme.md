## UV-Lamp

Almost Finsihed!

This respository hosts the UV lamp order tracking and reminder project

This system is composed of two main parts:

- The reminder system (Reminder.py), which is responsible for updating the local database and automatically sending out emails when needed
- The flask web app (Server.py), which is the web app responsible for letting contractors track/update their orders

### Structure
- Data.py
  * Manages the local sqlite3 database connection
- Emailer.py
  * Contains methods for sending out emails using the SendGrid API
- GoogleMapsAPI.py
  * Contains methods for connecting to and using the google maps API
  * Used for geolocation, address validation, and getting streetview images from addresses
- PGData.py
  * Manages connections to the ORO UAT5 PostgreSQL database
- Reminder.py
  * Responsible for updating order statuses, scheduling reminders, and sending out emails when needed
- Server.py
  * Hosts the flask web application
- config/
  * Contains JSON configuration files for the system
- container/
  * Contains several classes for conveient object-like handling of sqlite3 records
- static/
  - scripts/
    * Contains .js scripts used by flask server (pretty much never used)
  - stylesheets/
    * Contains .css files used by the flask server
- templates/
  - web/
    * Contains all the Jinja templates used by the flask server
  - email/
    * Contains all Jinja email templates to be sent out
   
### Python Dependencies
- sqlite3
- flask
- jinja2
- sendgrid
- psycopg2 (PostgreSQL)

### Usage
- Fill out credentials for Google Maps, ORO CRM, and Sendgrid connection within config/credentials.json
- To run the web server, run Server.py, and access through configured host
- To run the reminder system, run Reminder.py
