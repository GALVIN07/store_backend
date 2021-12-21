import pymongo
import json
from bson import obj, ObjectId

# connection string
mongo_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_url)

db = client.get_database("tacticalKaren")






class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)

        return json.JSONEncoder.default(obj)


def json_parse(data):
    return JSONEncoder().encode(data)