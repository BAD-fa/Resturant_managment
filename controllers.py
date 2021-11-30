from abc import ABC, abstractmethod
from models import Admin, Restaurant, Customer


class Controller(ABC):
    def __init__(self):
        self.user = None

    @abstractmethod
    def register(self, *args, **kwargs):
        pass

    @abstractmethod
    def login(self, username, password):
        pass

    def logout(self):
        self.user = None


class AdminController(Controller):
    def register(self, username, password, first_name, last_name, restaurant):
        if Admin.query.exist("username", username):
            raise Exception("Admin already exists !!!")
        else:
            restaurant = Restaurant.query.get("name", restaurant)
            if restaurant is None:
                raise Exception("Restaurant does not exist !!!")
            else:
                if len(restaurant.admins) < int(restaurant.max_admins):
                    admin = Admin(username, password, first_name, last_name)
                    admin.restaurant = restaurant
                    admin.save()
                    self.login(username, password)
                else:
                    raise Exception("This restaurant can't have anymore admin !!!")

    def login(self, username, password):
        admin = Admin.query.get("username", username)
        if admin is not None:
            if admin.password == password:
                self.user = admin
            else:
                raise Exception("Wrong password !!!")
        else:
            raise Exception("Admin doesn't exist please register first !!!")


class CustomerController(Controller):
    def register(self, username, password, first_name, last_name):
        if Customer.query.exist("username", username):
            raise Exception("Customer already exists !!!")
        else:
            customer = Customer(username, password, first_name, last_name)
            customer.save()
            self.login(username, password)

    def login(self, username, password):
        customer = Customer.query.get("username", username)
        if customer is not None:
            if customer.password == password:
                self.user = customer
            else:
                raise Exception("Wrong password !!!")
        else:
            raise Exception("Customer doesn't exist please register first !!!")

    @staticmethod
    def list_of_restaurant():
        list_of_restaurant = [elm.name for elm in Restaurant.query.load()]
        return list_of_restaurant


class RestaurantController:
    @staticmethod
    def register(name, max_admin):
        if Restaurant.query.exist("name", name):
            raise Exception("Restaurant already exists !!!")
        else:
            restaurant = Restaurant(name, max_admin)
            restaurant.save()
