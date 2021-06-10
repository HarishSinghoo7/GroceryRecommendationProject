from ecommerce.databases.models import Model


class OrderItem(Model):
    def __init__(self):
        super(OrderItem, self).__init__('Order_Item')

        # self.logPath = 'ecommerce/logs/customer'