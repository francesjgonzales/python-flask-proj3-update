import datetime
from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import certifi


load_dotenv(find_dotenv())

print (datetime.date.today())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://jen:{password}@studentdb.thkbj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where())

""" print all database names """
dbs = client.list_database_names()

""" print specific collection """
student_db = client.student
collections = student_db.list_collection_names()
print(collections)

def insert_student_doc():
    collection = student_db.profile
    profile_document = {
        "First Name": "Namjoo0n",
        "Last Name": "Kim",
        "Date of Birth (MM-DD-YYYY)": {
    "$date": (1995,12,4)
  }
    }
    inserted_id = collection.insert_one(profile_document).inserted_id
    print(inserted_id)

insert_student_doc()


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('base.template.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    
