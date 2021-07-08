from ecommerce.controllers import Controller
from ecommerce.databases.models.cart import Cart
import datetime

class CartController(Controller):
    def __init__(self):
        super(CartController, self).__init__()
        self.cart = Cart()

    def insert(self, form_data):
        """
        Description: Inserting data into customer_cart collection
        :return: customer_id
        """
        try:
            self.cart.create({
                "customer_id": form_data['customer_id'],
                "product_id": form_data['product_id'],
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            return self.get(form_data['customer_id'])
        except Exception as e:
            self.log("Error: "+str(e))



    def get(self, customer_id):
        """
        Description: fetching data from customer_cart collection
        :return: list of cart products
        """
        try:
            return self.cart.aggregate([
                {"$match": {"customer_id": customer_id}},
                {"$lookup": {
                    "from": 'Product',
                    "localField": 'product_id',
                    "foreignField": 'product_id',
                    "as": 'product'
                }}
            ])
        except Exception as e:
            self.log("Error: "+str(e))

    def remove(self, id):
        """
        Description: deleting data from customer_cart collection
        :return: MongoDB delete query response
        """
        try:
            return self.cart.delete_by_id(id)
        except Exception as e:
            self.log("Error: "+str(e))

    def delete_where(self, cond: dict = {}):
        """
        Description: deleting multiple data from customer_cart collection
        :return: MongoDB delete query response
        """
        try:
            return self.cart.delete_many(cond)
        except Exception as e:
            self.log("Error: "+str(e))