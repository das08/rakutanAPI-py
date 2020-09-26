from pymongo import MongoClient
import setting as env
from modules.DotDict import DotDict


class Database:
    __dbIP = env.db_ip
    __dbPort = env.db_port
    __dbUsername = env.db_username
    __dbPass = env.db_pass
    __dbName = env.db_name
    __dbClient = None
    __dbConn = None

    def __init__(self):
        """
        Initialization of Database
        """
        self.connect()

    def connect(self):
        """
        Connect to mongodb
        """
        uri = f"mongodb://{self.__dbUsername}:{self.__dbPass}@{self.__dbIP}:{self.__dbPort}"
        self.__dbClient = MongoClient(uri)
        self.__dbConn = self.__dbClient[self.__dbName]

    def disconnect(self):
        """
        Disconnect from mongodb
        """
        self.__dbClient.close()

    def find(self, colName, query: dict, projection=None):
        """
        Perform find action
        :param colName: (str) collection name
        :param query: (dict) query
        :param projection: (option) (dict) options to specify field
        :return: (dict)
        """
        res = DotDict({
            "result": None,
            "count": None,
            "queryResult": None
        })
        try:
            collection = self.__dbConn[colName]
            queryResults = collection.find(filter=query, projection=projection)
            count = collection.count_documents(filter=query)
            res.result = "success"
            res.count = count
            res.queryResult = queryResults
        except Exception as e:
            res.result = "exception"
        finally:
            return res

    def update(self, colName, query: dict):
        """
        Perform update action
        :param colName: (str) collection name
        :param query: (dict) query
        :return: (dict)
        """
        res = DotDict({
            "result": None,
            "count": None,
        })
        try:
            collection = self.__dbConn[colName]
            count = collection.find_one_and_update(query)['count']
            res.result = "success" if count > 0 else "fail"
            res.count = count
        except Exception as e:
            res.result = "exception"
        finally:
            return res

    def insert(self, colName, document: dict):
        """
        Perform insert action
        :param colName: (str) collection name
        :param document: (dict) document
        :return: (dict)
        """
        res = DotDict({
            "result": None
        })
        try:
            collection = self.__dbConn[colName]
            count = collection.insert_one(document)
            res.result = "success"
        except Exception as e:
            res.result = "exception"
        finally:
            return res

    def delete(self, colName, query: dict):
        """
        Perform delete action
        :param colName: (str) collection name
        :param query: (dict) query
        :return: (dict)
        """
        res = DotDict({
            "result": None,
            "count": None,
        })
        try:
            collection = self.__dbConn[colName]
            count = collection.delete_one(query).deleted_count
            res.result = "success" if count > 0 else "fail"
            res.count = count
        except Exception as e:
            res.result = "exception"
        finally:
            return res

    def exist(self, colName, query: str):
        """
        Check if specific document is in database
        :param colName: (str) collection name
        :param query: (dict) query
        :return: (Bool)
        """
        res = None
        try:
            collection = self.__dbConn[colName]
            count = collection.count_documents(filter=query)
            res = count > 0
        except Exception as e:
            res = False
        finally:
            return res
