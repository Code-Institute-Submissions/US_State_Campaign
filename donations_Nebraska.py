from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

#MONGODB_HOST = 'localhost'
#MONGODB_PORT = 27017
#DBS_NAME = 'donorsUSA'
#COLLECTION_NAME = 'projects'
#MONGO_URI = 'mongodb://root:donorusa@ds257245.mlab.com:57245/donors_usa'
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DBS_NAME = os.getenv('MONGO_DB_NAME', 'donorsUSA')
COLLECTION_NAME = 'projects'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route("/donorsUS/projects")
def donor_projects():
    """
    A Flask view to serve the project data from
    MongoDB in JSON format.
    """

    # A constant that defines the record fields that we wish to retrieve.
    FIELDS = {
        '_id': False, 'funding_status': True, 'school_state': True, 'secondary_focus_area': True,
        'resource_type': True, 'poverty_level': True, 'total_price_excluding_optional_support': True,
        'primary_focus_subject': True, 'teacher_prefix': True, 'primary_focus_area': True,
        'date_posted': True, 'num_donors': True, 'students_reached': True, 'total_donations': True
    }

    # Open a connection to MongoDB using a with statement such that the
    # connection will be closed as soon as we exit the with statement
    with MongoClient(MONGO_URI) as conn:
        # Define which collection we wish to access
        collection = conn[DBS_NAME][COLLECTION_NAME]
        # Retrieve a result set only with the fields defined in FIELDS
        # and limit the the results to 55000
        projects = collection.find(projection=FIELDS, limit=15000)
        # Convert projects to a list in a JSON object and return the JSON data
        return json.dumps(list(projects))

if __name__ == '__main__':
    app.run()