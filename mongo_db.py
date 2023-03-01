from bson import ObjectId
from pymongo import MongoClient
import os

class Mongo_process:
    MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
    connection_string = f"mongodb://vacancy:mongopass@{MONGO_HOST}:27017/"
    client = None
    db = None
    collection = None
    def __enter__(self):
        self.client = MongoClient(self.connection_string)
        self.db = self.client["vacancy"]
        self.collection = self.db["contacts"]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def insert_doc(self, document: dict):
        return self.collection.insert_one(document).inserted_id

    def get_doc(self, document_id):
        return self.collection.find_one({"_id": ObjectId(document_id)})

    def update_doc(self, document_id, doc:dict):
        self.collection.update_one({"_id": ObjectId(document_id)},{ "$set": doc})

if __name__ == "__main__":
    b=1
    with Mongo_process() as mongo:
        mongo.insert_doc({"name":"123"})
        obj = mongo.get_doc("63ff2bc83fda2b56e883cd3d")