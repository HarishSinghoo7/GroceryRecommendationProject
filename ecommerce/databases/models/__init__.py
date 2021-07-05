from ecommerce.databases import DBConnection
from bson.objectid import ObjectId


class Model(DBConnection):
    def __init__(self, collection):
        try:
            super(Model, self).__init__()
            self.collection = self.db[collection]
            self.hidden_fields = {}
        except Exception as e:
            raise Exception()

    def create(self, data: dict):
        """
        Description: Add single data in collection
        :param data: collection data dictionary
        :return: data add response
        """
        try:
            return list(self.collection.insert_one(data))
        except Exception as e:
            raise Exception()

    def create_multiple(self, data: list):
        """
        Description: Add multiple data in collection
        :param data: list of collection data dictionary
        :return: data add response
        """
        try:
            return list(self.collection.insert_many(data))
        except Exception as e:
            raise Exception()

    def find(self, cond: dict = {}, select: dict = {}):
        """
        Description: Fetch data from collection
        :param select: dictionary with collection field name and (0/1) value 0 means don't select the field
        :return: collection data object
        """
        try:
            if select:
                return self.collection.find(cond, select)
            else:
                return self.collection.find(cond, self.__select_dict())
        except Exception as e:
            raise Exception()

    def aggregate(self, cond: list):
        try:
            return list(self.collection.aggregate(cond))
        except Exception as e:
            raise Exception()

    def query(self, query: dict = {}):
        try:
            return list(self.collection.find(query))
        except Exception as e:
            raise Exception()

    def delete_by_id(self, id):
        try:
            return self.collection.delete_one({"_id": ObjectId(id)})
        except Exception as e:
            raise Exception()

    def delete(self, query: dict = {}):
        try:
            return self.collection.delete_one(query)
        except Exception as e:
            raise Exception()

    def delete_many(self, query: dict = {}):
        try:
            return self.collection.delete_many(query)
        except Exception as e:
            raise Exception()


    def __select_dict(self):
        return {field: 0 for field in self.hidden_fields}