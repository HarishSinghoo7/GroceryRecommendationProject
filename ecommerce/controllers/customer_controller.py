from ecommerce.controllers import Controller
from ecommerce.databases.models.customer import Customer
from ecommerce.databases.models.user_details import UserDetail
from flask_session import Session
import string
import random

class CustomerController(Controller):
    def __init__(self):
        self.customer = Customer()
        self.user_detail = UserDetail()

    def index(self):
        """
        Description: Fetch the list of customers
        :return: list of customers
        """
        customers = self.customer.find()
        return customers

    def login(self, form_param):
        """
        Description: Authenticate user credentials
        :parameter:
        @form_param: Login form values username and password
        :return: customer detail
        """
        email = form_param['email']
        password = form_param['password']
        customer_detial = self.user_detail.aggregate([
            {"$match": {"User_Id": email, "password": password}},
            {"$lookup":
                {
                    "from": 'Customer',
                    "localField": 'customer_id',
                    "foreignField": 'customer_id',
                    "as": 'customer'
                }
            }
        ])
        if customer_detial:
            return customer_detial[0]['customer']
        else:
            return False

    def register(self, form_param):
        """
        Description: Register new customer
        :parameter:
        @form_param: Registration form data
        :return: customer data
        """
        name = form_param['name']
        email = form_param['email']
        phone = form_param['phone']
        password = form_param['password']
        customer_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

        self.customer.create({
            "customer_id": customer_id,
            "customer name": name,
            "phone": phone,
        })
        self.user_detail.create({
            "User_Id": email,
            "customer_id": customer_id,
            "password": password
        })

        return self.customer.aggregate([{"$match":{'customer_id': customer_id}}])