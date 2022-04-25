from pymongo import MongoClient


class DataBase:
    def __init__(self):
        self.DBClient = MongoClient('mongodb://43.204.111.103:27017/')
        self.DB = self.DBClient.WebPilot
        self.CRCollection = self.DB.DataStore
        self.URLCollection = self.DB.URLStore
        self.LastURL = ""

    def addToContentRepository(self, keys=[], values=[], dataDict=None):
        if dataDict == None:
            dataDict = dict(zip(keys, values))
        success = self.CRCollection.insert_one(dataDict)
        return success

    def listContentRepository(self, key, value):
        data = self.CRCollection.find({key, value})
        return data

    def searchContentRepository(self, query):
        data = list(self.CRCollection.find({'$text': {'$search': query}}))
        return data

    def deleteFromContentRepository(self, id):
        success = self.CRCollection.remove({'_id': id})
        return success

    def addToURLStore(self, values):
        keys = len(values) * ["URL", ]
        dataDict = [{k: v} for k, v in zip(keys, values)]
        success = self.URLCollection.insert_many(dataDict)
        return success

    def listURLStore(self, key, value):
        data = self.URLCollection.find({key, value})
        return data

    def getFirstURL(self):
        data = self.URLCollection.find_one()
        inCR = self.CRCollection.find_one({'URL': data['URL']})
        if (inCR != None and inCR != "") or (data['URL'] == self.LastURL):
            self.deleteFromURLStore(data['_id'])
            return None
        self.LastURL = data['URL']
        return data

    def getXUrls(self, x):
        data = self.URLCollection.find({}).limit(x)
        return data

    def deleteFromURLStore(self, id):
        success = self.URLCollection.remove({'_id': id})
        return success

    def getURLID(self, URL):
        data = self.URLCollection.find_one({'URL': URL})
        return data['_id']
