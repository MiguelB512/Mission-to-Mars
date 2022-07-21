# Import dependencies for flask 
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


# Set up the flask application with variable 'app'
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Create the home route for the application, set the mars variable to find the 
# mars collection in out DB, return an HTML template using the index.html file, 
# and set mars = mars to tell python to use out mars collection. The first mars 
# is a variable, can be set to anything 
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


# Set up the second route, 'scrape', which calls a function that uses a button 
# to scrape the data from the scraping file. Mars set the db to the one we created
# and then the data is scraped and mars is updated using update_one to the new 
# data we get after scraping. Mars_data is holding the newly scraped data. 
# Upsert = True tells mongo to create a new document if one doesn't already exist.
# Return redirect will send us back to the / (home page) where we can see the updated content.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)


# Tell flask to run 
if __name__ == "__main__":
   app.run()