from ecommerce.controllers import Controller
from ecommerce.databases.models.category import Category

class CategoryController(Controller):
    def __init__(self):
        super(CategoryController, self).__init__()
        self.category = Category()

    def index(self):
        """
        Description: Will fetch categories in hierarchical order
        :return: list of categories
        """
        try:
            return self.category.aggregate([
                {
                    "$match": {"parent_category_id": None}
                },
                {
                    "$lookup":
                        {
                            "from": 'Product_Category',
                            "localField": 'product_category_id',
                            "foreignField": 'parent_category_id',
                            "as": 'child_categories'
                        }
                }
            ])
        except Exception as e:
            self.log("Error: "+str(e))

    def top_3_categories(self):
        """
        Description: Will fetch 3 categories from database
        :return: list of categories
        """
        try:
            return self.category.aggregate([
                    {"$match": {"parent_category_id": {"$ne": None}}},
                    {"$limit": 3}
                 ])
        except Exception as e:
            self.log("Error: "+str(e))

    def find_by_id(self, category_id):
        """
        Description: Find category based on category_id
        :return: Category data
        """
        try:
            return self.category.aggregate([{"$match":{'product_category_id': category_id}}])[0]
        except Exception as e:
            self.log("Error: "+str(e))