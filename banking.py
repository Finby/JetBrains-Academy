import random
import sqlite3


class BankingSystem:
    IIN_DEFAULT = '400000'
    CARD_DB = 'card.s3db'

    def __init__(self):
        self.logged_in = False
        self.user_choice = (None, None)
        # dictionary in format '{"account_card": {"PIN": pin_int, "balance": int}}'
        self.user_accounts_dict = {}
        self.account_card_current = None
        self.conn = None
        self.db_cursor = self.init_db()

    def init_db(self):
        self.conn = sqlite3.connect(self.CARD_DB)
        cursor = self.conn.cursor()
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='card';")
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute("""create table card 
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)""")
            self.conn.commit()
        return cursor

    def __initial_menu(self):
        user_input = -1
        while user_input not in ('0', '1', '2'):
            print("1. Create an account", "2. Log into account", "0. Exit", sep="\n")
            user_input = input()
            print()
            if user_input not in ('0', '1', '2'):
                print('Wrong choice. Repeat.')
        self.user_choice = (0, int(user_input))

    def __working_menu(self):
        user_input = -1
        while user_input not in ('0', '1', '2', '3', '4', '5'):
            print("1. Balance",
                  "2. Add income",
                  "3. Do transfer",
                  "4. Close account",
                  "5. Log out",
                  "0. Exit", sep="\n")
            user_input = input()
            print()
            if user_input not in ('0', '1', '2', '3', '4', '5'):
                print('Wrong choice. Repeat.')
        self.user_choice = (1, int(user_input))

    def do_close_account(self):
        self.db_cursor.execute("delete from card where number = {}".format(self.account_card_current))
        self.conn.commit()
        print()
        print("The account has been closed!")
        self.__log_out()

    def __do_action(self):
        if self.user_choice == (0, 1):
            self.do_create_account()
        elif self.user_choice == (0, 2):
            self.do_login()
        elif self.user_choice == (1, 1):
            self.print_balance()
        elif self.user_choice == (1, 2):
            self.add_income()
        elif self.user_choice == (1, 3):
            self.do_transfer()
        elif self.user_choice == (1, 4):
            self.do_close_account()
        elif self.user_choice == (1, 5):
            self.__log_out()

    def is_existing_card(self, card_num):
        self.db_cursor.execute("select count(*) from card where number = {}".format(card_num))
        result = self.db_cursor.fetchone()
        if result[0] == 0:
            return False
        else:
            return True

    def do_transfer(self):
        print("Transfer")
        card_number_to_transfer = input("Enter card number:")
        checksum = self.generate_checksum(card_number_to_transfer[:6], card_number_to_transfer[6:15])
        if checksum != int(card_number_to_transfer[-1]):
            print("Probably you made a mistake in the card number. Please try again!")
        elif not self.is_existing_card(card_number_to_transfer):
            print("Such a card does not exist.")
        else: # card number is valid do money transfer
            transfer_amount = int(input("Enter how much money you want to transfer:"))
            self.transfer_money(self.account_card_current, card_number_to_transfer, transfer_amount)

    def transfer_money(self, card_from, card_to, transfer_amount):
        self.db_cursor.execute("select balance from card where number = {}".format(card_from))
        balance_from = self.db_cursor.fetchone()
        if transfer_amount > balance_from[0]:
            print('Not enough money!')
        else:
            self.db_cursor.execute("""update card
                                            set balance = {}
                                            where number = {}""".format(balance_from[0] - transfer_amount,
                                                                        card_from)
                                   )
            self.db_cursor.execute("""update card
                                            set balance = balance + {}
                                            where number = {}""".format(transfer_amount,
                                                                        card_to)
                                   )
            self.conn.commit()
            print("Success!\n")


    def add_income(self):
        income_ = int(input("Enter income:"))
        self.db_cursor.execute("select balance from card where number = {}".format(self.account_card_current))
        result = self.db_cursor.fetchone()
        self.db_cursor.execute("""update card
                                set balance = {}
                                where number = {}""".format(result[0] + income_,
                                                            self.account_card_current)
                               )
        print("Income was added!")
        self.conn.commit()

    def print_menu(self):
        if self.logged_in is False:
            self.__initial_menu()
        else:
            self.__working_menu()

    @staticmethod
    def generate_checksum(iin_, middle_nine_symbols_):
        list_init = list(iin_ + middle_nine_symbols_)
        # 1 step of algorithm: make int() and double the numbers in odd positions.
        # odd position of card number is even index in list
        list_init_int_1 = [int(val) * 2 if i % 2 == 0 else int(val) for i, val in enumerate(list_init)]
        list_init_int_2 = [i - 9 if i > 9 else i for i in list_init_int_1]
        last_number = (10 - sum(list_init_int_2) % 10) % 10
        return last_number

    def do_create_account(self):
        iin = self.IIN_DEFAULT
        random.seed()
        middle_nine_symbols = random.randint(100000000, 999999999)
        checksum = self.generate_checksum(iin, str(middle_nine_symbols))
        account_card_current_ = str(iin) + str(middle_nine_symbols) + str(checksum)
        account_pin_current_ = random.randint(1000, 9999)
        # self.account_card_current = str(iin) + str(middle_nine_symbols) + str(checksum)
        # self.account_pin_current = random.randint(1000, 9999)
        print("Your card has been created")
        print("Your card number:", account_card_current_, sep="\n")
        print("Your card PIN:", account_pin_current_, sep="\n")
        print()
        self.check_and_store(account_card_current_, account_pin_current_)
        # self.user_accounts_dict[account_card_current_] = {'PIN': account_pin_current_,
        #                                                   'balance': 0}

    def check_and_store(self, card_number, card_pin):
        self.db_cursor.execute("select count(*) from card where number = {} and pin = {}".format(card_number, card_pin))
        result = self.db_cursor.fetchone()
        if result[0] == 0:
            card_id = random.randint(1, 10000)
            self.db_cursor.execute(
                "INSERT INTO card (number, pin) VALUES ({}, {})".format(card_number, card_pin))
            self.conn.commit()

    def do_login(self):
        input_card = input("Enter your card number:\n")
        input_pin = int(input("Enter your PIN:\n"))
        if self.is_valid_credentials(input_card, input_pin):
            print("You have successfully logged in!")
            print()
            self.logged_in = True
            self.account_card_current = input_card
        else:
            print("Wrong card number or PIN!")
            print()

    def is_valid_credentials(self, card_number, card_pin):
        self.db_cursor.execute("select count(*) from card where number = {} and pin = {}".format(card_number, card_pin))
        result = self.db_cursor.fetchone()
        if result[0] == 1:
            return True
        else:
            return False

    def print_balance(self):
        self.db_cursor.execute("select balance from card where number = {}".format(self.account_card_current))
        result = self.db_cursor.fetchone()
        print("Balance: {}".format(result[0]))
        print()

    def __log_out(self):
        self.logged_in = False
        self.account_card_current = None

    def bank_work_cycle(self):
        while True:
            self.print_menu()
            self.__do_action()
            if self.__is_exit():
                break
        self.do_full_exit()

    def do_full_exit(self):
        self.conn.commit()
        self.db_cursor.close()
        print("Bye!")

    def __is_exit(self):
        return bool(self.user_choice[1] == 0)


my_bank = BankingSystem()
my_bank.bank_work_cycle()
