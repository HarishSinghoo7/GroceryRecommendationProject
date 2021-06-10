from ecommerce.databases.models import Model


class UserDetail(Model):
    def __init__(self):
        super(UserDetail, self).__init__('User_details')

        # self.logPath = 'ecommerce/logs/customer'