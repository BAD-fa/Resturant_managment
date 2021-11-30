from controllers import AdminController, CustomerController, RestaurantController
from models import *
import os


class App:
    def __init__(self):
        self._admin_controller = None
        self._customer_controller = None
        self._restaurant_controller = None

    @property
    def admin_controller(self):
        return self._admin_controller

    @property
    def customer_controller(self):
        return self._customer_controller

    @property
    def restaurant_controller(self):
        return self._restaurant_controller

    @admin_controller.setter
    def admin_controller(self, controller: AdminController):
        self._admin_controller = controller

    @customer_controller.setter
    def customer_controller(self, controller: CustomerController):
        self._customer_controller = controller

    @restaurant_controller.setter
    def restaurant_controller(self, controller: RestaurantController):
        self._restaurant_controller = controller

    @staticmethod
    def clear():
        os.system('clear')


if __name__ == "__main__":
    app = App()

    customer_controller = CustomerController()
    admin_controller = AdminController()
    restaurant_controller = RestaurantController()

    app.customer_controller = customer_controller
    app.admin_controller = admin_controller
    app.restaurant_controller = restaurant_controller

    print("""
    
                Hello ..... Welcome to Behrad Restaurant Managment 
    
    """)

    while True:

        op = input("Do you want to add Restaurant? (y/n)\n")
        while op == "y":
            restaurant_name = input("Enter name of restaurant: ")
            max_admins = input("Enter maximum number of Admins: ")
            app.restaurant_controller.register(restaurant_name, max_admins)
            op = input("Do you wat to continue? (y/n)")

        while True:
            op = input("Do you want to REGISTER or LOGIN? (R/L)\n")

            if op == "R":
                t = input("Do you want to register as ADMIN or CUSTOMER? (A/C)\n")
                if t == "A":
                    username = input("please enter your username: ")
                    password = input("please enter your password: ")
                    first_name = input("please enter your first name: ")
                    last_name = input("please enter your last name: ")
                    restaurant = input("please enter your restaurant: ")
                    app.admin_controller.register(username, password, first_name, last_name, restaurant)
                    app.clear()
                    break

                elif t == "C":
                    username = input("please enter your username: ")
                    password = input("please enter your password: ")
                    first_name = input("please enter your first name: ")
                    last_name = input("please enter your last name: ")
                    app.customer_controller.register(username, password, first_name, last_name)
                    app.clear()
                    break

                else:
                    app.clear()
                    print("Wrong type please try again !!!")
                    continue

            elif op == "L":
                t = input("Do you want to login as ADMIN or CUSTOMER? (A/C)\n")
                if t == "A":
                    username = input("please enter your username: ")
                    password = input("please enter your password: ")
                    app.admin_controller.login(username, password)
                    app.clear()
                    break

                if t == "C":
                    username = input("please enter your username: ")
                    password = input("please enter your password: ")
                    app.customer_controller.login(username, password)
                    app.clear()
                    break

                else:
                    app.clear()
                    print("Wrong type please try again !!!")
                    continue

            else:
                app.clear()
                print("Wrong operation please try again !!!")
                continue

        while True:
            if t == "A":
                print("""

                        ADMIN PANEL

                """)

                op = int(input(
                    "What do you want to do?\n1.Add food\n2.Remove food\n3.List of Customer\n4.Menu\n5.clear\n6.Exit\n"))
                if op == 1:
                    food_name = input("Enter name of the food: ")
                    count = int(input("Enter count of food: "))
                    price = int(input("Enter price of food: "))
                    app.admin_controller.user.add_food(food_name, price, count)

                elif op == 2:
                    food_name = input("Enter name of the food: ")
                    app.admin_controller.user.remove_food(food_name)

                elif op == 3:
                    for elm in app.admin_controller.user.list_of_customers():
                        print(elm.first_name + ' ' + elm.last_name)

                elif op == 4:
                    for k, v in app.admin_controller.user.menu().items():
                        print(k, v)

                elif op == 5:
                    app.clear()

                elif op == 6:
                    app.customer_controller.logout()
                    break

                else:
                    app.clear()
                    print("Wrong operation try again !!!")
                    continue

            elif t == "C":

                print(f"""

                                    {app.customer_controller.user.first_name + ' ' + app.customer_controller.user.last_name}

                            """)

                op = int(input(
                    "What do you want to do?\n1.List of restaurants\n2.Choose restaurant\n3.Menu\n4.Order\n5.Bill\n6.History\n7.clear\n8.Exit\n"))

                if op == 1:
                    for elm in app.customer_controller.list_of_restaurant():
                        print(elm)

                elif op == 2:
                    restaurant_name = input("Enter name of the restaurant: ")
                    app.customer_controller.user.set_restaurant(restaurant_name)

                elif op == 3:
                    if app.customer_controller.user.restaurant is not None:
                        for k, v in app.customer_controller.user.restaurant.menu.items():
                            print(k, v)
                    else:
                        app.clear()
                        print("Please choose a restaurant first !!!")
                        continue

                elif op == 4:
                    if app.customer_controller.user.restaurant is not None:
                        if app.customer_controller.user.can_order:

                            temp = "y"
                            while temp == "y":

                                for k, v in app.customer_controller.user.restaurant.menu.items():
                                    print(k, v)

                                food_name = input("Enter a food name: ")
                                count = int(input("How many do you want? "))
                                if food_name in app.customer_controller.user.restaurant.menu.keys():
                                    if count > app.customer_controller.user.restaurant.menu[food_name][1]:
                                        print("Not enough food order less or another food !!!")
                                        continue
                                    else:
                                        app.customer_controller.user.order(food_name, count)
                                else:
                                    print("Food is not in menu choose another one !!!")
                                    continue
                                temp = input("Do you want to continue? (y/n)")
                            app.customer_controller.user.can_order = False
                        else:
                            app.clear()
                            print("please pay the bill first !!!")
                            continue
                    else:
                        app.clear()
                        print("Please choose a restaurant first !!!")
                        continue

                elif op == 5:
                    print(app.customer_controller.user.bill)
                    t_op = input("Do you want to pay the bill? (y/n)")
                    if t_op == "y":
                        app.customer_controller.user.pay_bill()
                    if t_op == "n":
                        app.clear()
                        continue

                elif op == 6:
                    for k, v in app.customer_controller.user.history_of_orders.items():
                        print(k, v)

                elif op == 7:
                    app.clear()

                elif op == 8:
                    app.customer_controller.logout()
                    break

                else:
                    app.clear()
                    print("Wrong operation try again !!!")
                    continue

        ope = input("Do you want to exit? (y/n)")

        if ope == "y":
            break

        else:
            continue

    print("GoodBye")

