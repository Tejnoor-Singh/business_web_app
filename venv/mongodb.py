import pymongo


class MongoDBHelper:

    def __init__(self, collection='registered'):
        uri = "mongodb+srv://tejnoorsingh:tejnoor7868@cluster0.9sfdgrz.mongodb.net/?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        self.db = client['fateh']
        self.collection = self.db[collection]
        print("mongodb connected")

    def insert(self, document):
        result = self.collection.insert_one(document)
        print("DOCUMENT INSERTED", result)
        return result

    def delete(self, query):
        result = self.collection.delete_one(query)
        print("Document Deleted:", result)

    def fetch(self, query=""):
        documents = self.collection.find(query)
        return list(documents)

    def update(self, document, query):
        update_query = {'$set': document}
        result = self.collection.update_many(query, update_query)
        print("updated document : ", result.modified_count)
