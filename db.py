from pymongo import MongoClient
import setting as env


class Database:
    __dbIP = env.db_ip
    __dbUsername = env.db_username
    __dbPass = env.db_pass

    def __init__(self, db_name, db_collection):
        self.__dbName = db_name
        self.__dbCollection = db_collection

    def connect(self):
        pass

    def disconnect(self):
        pass

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
