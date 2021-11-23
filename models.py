from uuid import uuid4
from typing import Dict, List
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
        self.password = self.set_password(password)
        self.id = self.set_id()

    def see_profile(self):
        return self.first_name + ' ' + self.last_name + '\n' + self.username + '\n' + self.type

    @staticmethod
    def set_password(password):
        return hash(password)

    @staticmethod
    def set_id():
        return uuid4()

    def save(self):
        try:
            with open(USER_DATA_PATH / self.file_name, "ab") as db_file:
                pickle.dump(self, db_file)

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
    menu: Dict[str, List] = {}
    customers: List[User] = []
    admins: List[User] = []

    def __init__(self, name: str):
        self.name = name

    def __call__(self):
        return self.name

    def update_menu(self, food_name: str, count: int):
        self.menu[food_name][1] -= count

    def save(self):
        try:
            with open(RESTAURANTS_DATA_PATH / self.file_name, "ab") as db_file:
                pickle.dump(self, db_file)

        except Exception as e:
            print(e)


class Admin(User):
    file_name = "admin.db"
    file_path = USER_DATA_PATH / file_name
    type = "Admin"

    def __init__(self, username: str, password: str, first_name: str, last_name: str, restaurant: Restaurant):
        super().__init__(username, password, first_name, last_name)
        self.restaurant = restaurant
        self.restaurant.admins.append(self)

    def menu(self):
        return self.restaurant.menu

    def add_food(self, name: str, price: int, count: int):
        food = Food(name, price)
        self.restaurant.menu[food.name] = [food.price, count]

    def edit_menu(self, food_name: str, count: int):
        self.restaurant.menu[food_name][1] = count

    def remove_food(self, food_name: str):
        self.restaurant.menu.pop(food_name)

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
    restaurant = None
    history_of_orders: Dict[int, Dict] = {}
    orders: Dict[str, int] = {}
    bill = 0
    can_order = True

    def set_restaurant(self, restaurant_name):
        self.restaurant = restaurant_name
        # self.restaurant.customers.append[self]

    def order(self, food_name: str, count: int):
        price = self.restaurant.menu[food_name][0]
        self.orders[food_name] = count
        self.restaurant.update_menu(food_name, count)
        self.bill += price * count

    def pay_bill(self):
        self.history_of_orders[self.bill] = self.orders
        self.can_order = True
        self.bill = 0
        self.orders = {}
        # self.restaurant.save()
        self.restaurant = None
        # self.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


R1 = Restaurant("Asghar sag Paz")
ad = Admin("behrad", "abcd1234", "Behrad", "Fathi", R1)
ad.add_food("food1", 12000, 5)
ad.add_food("food2", 15000, 4)
c1 = Customer("user1", "password1", "name1", "last1")
c1.set_restaurant(R1)
c1.order("food1", 3)
c1.order("food2", 2)
c1.pay_bill()
print(c1.bill)
print(R1.menu)

