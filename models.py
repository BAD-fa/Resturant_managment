import pickle
from uuid import uuid4
from typing import Dict, List, Set
import pickle

from db import BaseQuery
from settings import USER_DATA_PATH, RESTAURANTS_DATA_PATH


class Meta(type):
    def __init__(cls, *args, **kwargs):
        cls.query = BaseQuery(cls.file_path)
        super().__init__(*args, **kwargs)


'''    User    '''


class User(metaclass=Meta):
    file_name = None
    file_path = None
    type = None

    def __init__(self, username: str, password: str, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.restaurant = None
        self.id = self.set_id()

    def see_profile(self):
        return self.first_name + ' ' + self.last_name + '\n' + self.username + '\n' + self.type

    @staticmethod
    def set_password(password):
        return hash(password)

    @staticmethod
    def set_id():
        return str(uuid4())

    def save(self):
        try:
            with open(USER_DATA_PATH / self.file_name, "ab+") as db_file:
                if self.query.get("username", self.username) is None:
                    pickle.dump(self, db_file)
                else:
                    data_list = [elm for elm in self.query.load()]
                    db_file.seek(0)
                    db_file.truncate()
                    for elm in data_list:
                        if elm.username == self.username:
                            pickle.dump(self, db_file)
                        else:
                            pickle.dump(elm, db_file)

        except Exception as e:
            print(e)


'''     Food    '''


class Food:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    def __str__(self):
        return self.name


'''     Restaurant     '''


class Restaurant(metaclass=Meta):
    file_name = "restaurants.db"
    file_path = RESTAURANTS_DATA_PATH / file_name

    def __init__(self, name: str, max_admins: int):
        self.name = name
        self.menu: Dict[str, List] = {}
        self.customers: List[User] = []
        self.admins: List[User] = []
        self.max_admins = max_admins

    def __call__(self):
        return self.name

    def update_menu(self, food_name: str, count: int):
        self.menu[food_name][1] -= count
        self.save()

    def save(self):
        try:
            with open(RESTAURANTS_DATA_PATH / self.file_name, "ab+") as db_file:
                if self.query.get("name", self.name) is None:
                    pickle.dump(self, db_file)
                else:
                    data_list = [elm for elm in self.query.load()]
                    db_file.seek(0)
                    db_file.truncate()
                    for elm in data_list:
                        if elm.name == self.name:
                            pickle.dump(self, db_file)
                        else:
                            pickle.dump(elm, db_file)

        except Exception as e:
            print(e)


class Admin(User):
    file_name = "admin.db"
    file_path = USER_DATA_PATH / file_name
    type = "Admin"

    # def __init__(self, username: str, password: str, first_name: str, last_name: str, restaurant_name: str):
    #     super().__init__(username, password, first_name, last_name)
    #     self.set_restaurant(restaurant_name)
    #
    # def set_restaurant(self, restaurant_name):
    #     print(Restaurant.query.get("name", restaurant_name).name)
    #     self.restaurant = Restaurant.query.get("name", restaurant_name)
    #     self.restaurant.admins.append(self)

    def menu(self):
        return self.restaurant.menu

    def add_food(self, name: str, price: int, count: int):
        food = Food(name, price)
        self.restaurant.menu[food.name] = [food.price, count]
        self.restaurant.save()

    def remove_food(self, food_name: str):
        self.restaurant.menu.pop(food_name)
        self.restaurant.save()

    def list_of_customers(self):
        return self.restaurant.customers

    @staticmethod
    def list_of_customer_current_order(username: str):
        customer = Customer.query.get("username", username)
        return customer.orders

    @staticmethod
    def history_order_of_customer(username: str):
        customer = Customer.query.get("username", username)
        return customer.history_of_orders


class Customer(User):
    file_name = "customer.db"
    file_path = USER_DATA_PATH / file_name
    type = "Customer"

    def __init__(self, username: str, password: str, first_name: str, last_name: str):
        super().__init__(username, password, first_name, last_name)
        self.history_of_orders: Dict[int, Dict] = {}
        self.orders: Dict[str, int] = {}
        self.bill = 0
        self.can_order = True

    def set_restaurant(self, restaurant_name: str):
        self.restaurant = Restaurant.query.get("name", restaurant_name)
        self.restaurant.customers.append(self)
        self.save()

    def order(self, food_name: str, count: int):
        price = self.restaurant.menu[food_name][0]
        self.orders[food_name] = count
        self.restaurant.update_menu(food_name, count)
        self.bill += price * count
        self.save()

    def pay_bill(self):
        self.history_of_orders[self.bill] = self.orders
        self.can_order = True
        self.bill = 0
        self.orders = {}
        self.restaurant.save()
        self.restaurant = None
        self.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# for k, v in Customer.query.get("username", "jjj").history_of_orders.items():
#     print(k, v)
# print([elm.username for elm in Customer.query.load()])
# print([elm.username for elm in Admin.query.load()])
