from flask import Flask
from dotenv import load_dotenv
import os
import pprint
from pymongo import MongoClient

load_dotenv()

mongoURL = os.getenv("MONGODB_URL")

client = MongoClient(mongoURL)
dbs = client.list_database_names()
print(dbs)


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

