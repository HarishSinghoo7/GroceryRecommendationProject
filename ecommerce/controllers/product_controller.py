from ecommerce.controllers import Controller
from ecommerce.databases.models.product import Product

class ProductController(Controller):
    def __init__(self):
        self.product = Product()

    def index(self):
        return self.product.find()

    def top_products(self):
        return self.product.aggregate([{"$limit": 8}])

    def product_by_category_id(self, category_id):
        return self.product.aggregate([{"$match": {"product_category_id": category_id}}])

    def find_by_id(self, product_id):
        return self.product.aggregate([{"$match": {"product_id": product_id}}])[0]

    def search_products(self, params):
        keyword = params.args['keyword']
        category = params.args['category']

        if category == 'all':
            return self.product.aggregate([{"$match": {"product_name": keyword}}])
        else:
            return self.product.aggregate([{"$match": {"product_name": keyword, "product_category_id": category}}])