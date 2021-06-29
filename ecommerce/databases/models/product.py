from ecommerce.databases.models import Model


class Product(Model):
    def __init__(self):
        super(Product, self).__init__('Product')
        # self.logPath = 'ecommerce/logs/customer'

    def _get_search_query(self, params):
        """
        Description: This method is to create DB query from filter parameters
        :return: MongoDB search query object
        """
        keyword = params.args.get('keyword')
        category = params.args.get('category')
        min_price = params.args.get('min_price')
        max_price = params.args.get('max_price')
        instock = params.args.get('instock')
        qry = {}
        if keyword:
            qry['product_name'] = keyword
        if category != 'all':
            qry['product_category_id'] = category
        if instock:
            qry['product_qty'] = {"$gt": 0}
        if min_price and max_price:
            qry["product_price"] = {"$gt": int(min_price), "$lt": int(max_price)}

        return qry