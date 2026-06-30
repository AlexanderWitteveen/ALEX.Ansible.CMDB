from pymongo import MongoClient

class cmdbmongodb:
    def __init__(self, environmentid, ipaddress, username, password):
        # self.environmentid = environmentid
        self.connectionstring="mongodb://" + username + ":" + password + "@" + ipaddress + ":27017/?tls=true&tlsInsecure=true&authSource=admin"
        self.writer=MongoClient(self.connectionstring)
        self.db=self.writer["cmdb-" + environmentid]

    def clearcmdb(self):
        for collectionname in self.db.list_collection_names():
            collection = self.db[collectionname]
            collection.drop()

    def createindexes(self, collectionname, uniqueindex):
        collection=self.db[collectionname]
        for index in uniqueindex:
            collection.create_index(index, unique=True)

    # Consider rewrite see importinventory.py for example of merge strategy
    def mergedata(self, collectionname, key, allnewrecords):
        collection=self.db[collectionname]
        alloldrecords=collection.find({"IsMasterData": True})
        for oldrecord in alloldrecords:
            if oldrecord[key] not in [record[key] for record in allnewrecords]:
                collection.delete_one({key: oldrecord[key]})
        for newrecord in allnewrecords:
            newrecord["IsMasterData"]=True
            oldrecord=collection.find_one({key: newrecord[key]})
            if oldrecord:
                for field in newrecord:
                    oldrecord[field] = newrecord[field]
                collection.replace_one({key: oldrecord[key]}, oldrecord)
            else:
                collection.insert_one(newrecord)

    def droprecords(self, collectionname):
        collection=self.db[collectionname]
        collection.delete_many({})

    def appendrecord(self, collectionname, record):
        collection=self.db[collectionname]
        try:
            collection.insert_one(record)
        except Exception as e:
            pass


