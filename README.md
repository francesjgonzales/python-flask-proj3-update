# python-flask-proj3-update

## Run locally

`flask --app app run`

## How to connect MongoDB

1. Create a new cluster in MongoDB.
2. Connect via MongoDb Compass GUI.
3. Add password variable in .env
4. Copy connection string from MongoDB to VS code.

## MongoDB NoSQL database

- in BSON format similar to JSON
- allows frequent updates
- performs faster performance and scale easily
- Structure:
  ├── Database # Cluster contains database
  │ ├── Collections # Each database contains a number of collections
  │ ├──├── Documents # Stores KEY and VALUE pair per unique ID

## Encountered issues and how it was resolved

1. `SSL: CERTIFICATE_VERIFY_FAILED` - added `tlsCAFile=certifi.where()` in connection string. [documentation](https://stackoverflow.com/questions/68123923/pymongo-ssl-certificate-verify-failed-certificate-verify-failed-unable-to-ge)
