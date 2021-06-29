from ecommerce.controllers import Controller
from ecommerce.databases.models.cart import Cart
import datetime

class CartController(Controller):
    def __init__(self):
        self.cart = Cart()

    def insert(self, form_data):
        """
        Description: Inserting data into customer_cart collection
        :return: customer_id
        """
        self.cart.create({
            "customer_id": form_data['customer_id'],
            "product_id": form_data['product_id'],
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return self.get(form_data['customer_id'])



    def get(self, customer_id):
        """
        Description: fetching data from customer_cart collection
        :return: list of cart products
        """
        return self.cart.aggregate([
            {"$match": {"customer_id": customer_id}},
            {"$lookup": {
                "from": 'Product',
                "localField": 'product_id',
                "foreignField": 'product_id',
                "as": 'product'
            }}
        ])

    def remove(self, id):
        """
        Description: deleting data from customer_cart collection
        :return: MongoDB delete query response
        """
        return self.cart.delete_by_id(id)

    def delete_where(self, cond: dict = {}):
        """
        Description: deleting multiple data from customer_cart collection
        :return: MongoDB delete query response
        """
        return self.cart.delete_many(cond)