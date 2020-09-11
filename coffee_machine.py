class CoffeeMachine:
    def __init__(self):
        self.existing_water = 400
        self.existing_milk = 540
        self.existing_coffee_beans = 120
        self.existing_money = 550
        self.existing_disposable_cups = 9

    def fill_coffee_machine(self):
        water = int(input('Write how many ml of water do you want to add:'))
        self.existing_water += water
        milk = int(input('Write how many ml of milk do you want to add:'))
        self.existing_milk += milk
        coffee_beans = int(input('Write how many grams of coffee beans do you want to add:'))
        self.existing_coffee_beans += coffee_beans
        disposable_cups = int(input('Write how many disposable cups of coffee do you want to add:'))
        self.existing_disposable_cups += disposable_cups

    def coffee_machine_menu(self):
        print()
        action = input('Write action (buy, fill, take, remaining, exit):')
        while self.do_action(action):
            print()
            action = input('Write action (buy, fill, take, remaining, exit):')


    def withdraw_money_from_machine(self):
        print('I gave you ${}'.format(self.existing_money))
        self.existing_money = 0

    def do_action(self, action):
        if action == 'buy':
            self.order_coffee()
        elif action == 'fill':
            self.fill_coffee_machine()
        elif action == 'take':
            self.withdraw_money_from_machine()
        elif action == 'remaining':
            self.print_machine_status()
        elif action == 'exit':
            return False
        else:
            print('Unsupported operation')
            return False
        return True

    def print_machine_status(self):
        print()
        print('The coffee machine has:')
        print('{} of water'.format(self.existing_water))
        print('{} of milk'.format(self.existing_milk))
        print('{} of coffee beans'.format(self.existing_coffee_beans))
        print('{} of disposable cups'.format(self.existing_disposable_cups))
        print('{} of money'.format(self.existing_money))

    def order_coffee(self):
        print()
        coffee_name = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        if coffee_name == '1':
            coffee_ordered = Espresso()
        elif coffee_name == '2':
            coffee_ordered = Latte()
        elif coffee_name == '3':
            coffee_ordered = Cappuccino()
        elif coffee_name == 'back':
            return None
        else:
            print('There is not such coffee...')
            return None

        if self.can_do_coffee(coffee_ordered):
            print('I have enough resources, making you a coffee!')
            self.prepare_coffee(coffee_ordered)
        else:
            print('Sorry, not enough {}!'.format(self.not_enough_resource(coffee_ordered)))

    def not_enough_resource(self, coffee_type):
        missing_ingredients = []
        if self.existing_water < coffee_type.water:
            missing_ingredients.append('water')
        if self.existing_milk < coffee_type.milk:
            missing_ingredients.append('milk')
        if self.existing_coffee_beans < coffee_type.coffee_beans:
            missing_ingredients.append('coffee beans')
        if self.existing_disposable_cups < coffee_type.disposable_cups:
            missing_ingredients.append('disposable cups')
        if missing_ingredients:
            return ', '.join(missing_ingredients)
        else:
            return None


    def prepare_coffee(self, coffee_type):
        self.existing_water -= coffee_type.water
        self.existing_milk -= coffee_type.milk
        self.existing_coffee_beans -= coffee_type.coffee_beans
        self.existing_money += coffee_type.money
        self.existing_disposable_cups -= coffee_type.disposable_cups

    def can_do_coffee(self, coffee_type):
        return bool(self.existing_water >= coffee_type.water
                    and self.existing_milk >= coffee_type.milk
                    and self.existing_coffee_beans >= coffee_type.coffee_beans
                    and self.existing_disposable_cups >= coffee_type.disposable_cups)

    def check_reserves(self, received_order_caps):
        if received_order_caps == self.maximum_caps:
            print("Yes, I can make that amount of coffee")
        elif received_order_caps > self.maximum_caps:
            print(f"No, I can make only {self.maximum_caps} cups of coffee")
        else:
            print("Yes, I can make that amount of coffee "
                  f"(and even {self.maximum_caps - received_order_caps} more than that)")

    def calculate_maximum_caps(self):
        caps_number = self.existing_water // CoffeeOrder.WATER
        caps_number = min(caps_number, self.existing_milk // CoffeeOrder.MILK)
        caps_number = min(caps_number, self.existing_coffee_beans // CoffeeOrder.COFFEE_BEANS)
        return caps_number

class Coffee:
    def __init__(self, water=0, milk=0, coffee_beans=0, money=0):
        self.water = water
        self.milk = milk
        self.coffee_beans = coffee_beans
        self.money = money
        self.disposable_cups = 1

    def print_order(self):
        print(f'{self.water} ml of water')
        print(f'{self.milk} ml of milk')
        print(f'{self.coffee_beans} ml of coffee beans')
        print(f'{self.money} of money')
        print(f'{self.disposable_cups} of disposable cups')

class Espresso(Coffee):
    def __init__(self):
        Coffee.__init__(self, water=250, milk=0, coffee_beans=16, money=4)

class Latte(Coffee):
    def __init__(self):
        Coffee.__init__(self, water=350, milk=75, coffee_beans=20, money=7)

class Cappuccino(Coffee):
    def __init__(self):
        Coffee.__init__(self, water=200, milk=100, coffee_beans=12, money=6)



# messages = ('Starting to make a coffee',
#             'Grinding coffee beans',
#             'Boiling water',
#             'Mixing boiled water with crushed coffee beans',
#             'Pouring coffee into the cup',
#             'Pouring some milk into the cup',
#             'Coffee is ready!')
#
# print('\n'.join(messages))
my_machine = CoffeeMachine()
# my_order = CoffeeOrder()

# my_machine.print_machine_status()
my_machine.coffee_machine_menu()
# my_machine.print_machine_status()

# my_order.print_order()
