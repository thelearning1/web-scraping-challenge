from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo

#set up the flask server
app = Flask(__name__, template_folder='templates')

#setup mongo connection
conn = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app,conn)

#set routes for the page
@app.route('/')
def homepage():
    
    #query the mongo database to pass mars data to html
    mars_data = mongo.db.collection.find_one()

    #return the data with a render template
    return render_template("index.html",content=mars_data)


@app.route('/scrape')
def scrape_data():
    
    #import the scrape function
    from scrape_mars import scrape

    #pull the data from scrape_mars
    mars_info = scrape()

    #update the mongo db
    mongo.db.collection.update_one({},{"$set":mars_info},upsert=True)

    #redirect back to the homepage
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)