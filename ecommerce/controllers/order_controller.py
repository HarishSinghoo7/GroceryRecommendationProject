from ecommerce.controllers import Controller
from ecommerce.databases.models.order import Order
from ecommerce.databases.models.order_item import OrderItem
from ecommerce.controllers.cart_controller import CartController

import random
import string
import datetime

class OrderController(Controller):
    def __init__(self):
        self.order = Order()
        self.order_item = OrderItem()
        self.cart = CartController()

    def insert(self, customer_id):
        """
        Description: Creating new order
        :parameter
        @customer_id: Authenticated customer id
        :return: order_id
        """
        try:
            order_id = str(''.join(random.choices(string.ascii_lowercase + string.digits, k=32)))
            self.order.create({
                'order_id': order_id,
                'customer_id': customer_id,
                'order_status': 'Pending',
                'order_purchase_timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            cart = self.cart.get(customer_id)
            order_items = []
            for pro in cart:
                order_items.append({
                    'order_id': order_id,
                    'product_id': pro['product'][0]['product_id'],
                    'product_price': pro['product'][0]['product_price']
                })

            self.order_item.create_multiple(order_items)
            self.cart.delete_where({"customer_id": customer_id})
            return order_id
        except Exception as e:
            self.log("Error: "+str(e))


    def get(self, order_id):
        """
        Description: Fetching order details
        :parameter
        @order_id: order id
        :return: order details
        """
        try:
            return self.order.aggregate([
                {"$match": {"order_id": order_id}},
                {"$lookup": {
                    "from": 'Order_Item',
                    "localField": 'order_id',
                    "foreignField": 'order_id',
                    "as": 'order_items'
                }},
                {"$lookup": {
                    "from": 'Product',
                    "localField": 'order_items.product_id',
                    "foreignField": 'product_id',
                    "as": 'product'
                }}
            ])
        except Exception as e:
            self.log("Error: "+str(e))