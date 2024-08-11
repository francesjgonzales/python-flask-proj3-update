from flask import Flask
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import certifi

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://jen:{password}@studentdb.thkbj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where())

""" print all database names """
dbs = client.list_database_names()

""" print specific collection """
student_db = client.student
collection = student_db.list_collection_names()
print(collection)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

