from ecommerce.databases.models import Model


class Product(Model):
    def __init__(self):
        super(Product, self).__init__('Product')

        # self.logPath = 'ecommerce/logs/customer'