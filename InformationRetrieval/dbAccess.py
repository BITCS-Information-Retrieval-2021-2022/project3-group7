import pymongo
from bson.objectid import ObjectId


class DBAccess:
    def __init__(self, **kwargs):
        self.hosts = kwargs['hosts']
        self.port = kwargs['port']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.dbName = kwargs['db_name']
        self.docName = kwargs['doc_name']
        connectString = "mongodb://{}:{}@{}:{}/{}".format(self.user, self.password, self.hosts, self.port, self.db_name)
        self.dbClient = pymongo.MongoClient(connectString)
        self.db = self.dbClient[self.dbName]
        self.doc = self.db[self.docName]

    def search(self, query):
        idList = query['hits']['hit']
        res = []
        for id in idList:
            dbQuery = {"_id": id if isinstance(id, ObjectId) else ObjectId(id)}
            res.append(self.doc.find_one(dbQuery))
        self.reformatResult(res)
        query['hits']['hit'] = res
        return query

    def reformatResult(self, res):
        """
        According to res, change value type to return.
        :param res: result
        :return: reformatted result
        """

    def __del__(self):
        self.dbClient.close()
        print("Notice from DBAccess: MongoDB connection is closed.")