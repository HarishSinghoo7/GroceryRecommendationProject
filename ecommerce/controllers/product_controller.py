from ecommerce.controllers import Controller
from ecommerce.databases.models.product import Product

class ProductController(Controller):
    def __init__(self):
        super(ProductController, self).__init__()
        self.product = Product()

    def index(self):
        """
        Description: This method is to fetch the products list
        :return: list of products
        """
        try:
            return self.product.find()
        except Exception as e:
            self.log("Error: "+str(e))

    def top_products(self):
        """
        Description: This method is to fetch list of top 8 products
        :return: list of 8 products
        """
        try:
            return self.product.aggregate([{"$limit": 8}])
        except Exception as e:
            self.log("Error: "+str(e))

    def product_by_category_id(self, category_id, params=None):
        """
        Description: This method is to fetch list of products based on their category id
        :return: list of products
        """
        try:
            search_qry = []
            if params:
                search_qry = (self.product._get_search_query(params))
            search_qry['product_category_id'] = category_id
            return self.product.aggregate([{"$match": search_qry}])
        except Exception as e:
            self.log("Error: "+str(e))

    def find_by_id(self, product_id):
        """
        Description: This method is to fetch product based on product_id
        :return: product object
        """
        try:
            return self.product.aggregate([{"$match": {"product_id": product_id}}])[0]
        except Exception as e:
            self.log("Error: "+str(e))

    def search_products(self, params):
        """
        Description: This method is to find product based on search options
        :return: list of products
        """
        try:
            search_qry = self.product._get_search_query(params)
            return self.product.aggregate([{"$match": search_qry}])
        except Exception as e:
            self.log("Error: "+str(e))