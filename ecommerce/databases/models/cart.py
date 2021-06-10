from ecommerce.databases.models import Model


class Cart(Model):
    def __init__(self):
        super(Cart, self).__init__('customer_cart')

        # self.logPath = 'ecommerce/logs/customer'