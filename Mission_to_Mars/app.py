from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    my_data = mongo.db.my_data.find_one()
    return render_template("index.html", my_data=my_data)


@app.route("/scrape")
def scraper():
    my_data = mongo.db.my_data
    my_data_stuff = scrape_mars.scrape()
    my_data.update({}, my_data_stuff, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
