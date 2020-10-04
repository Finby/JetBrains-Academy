import random


class RockPaperScissors:
    RATING_FILE = 'rating.txt'
    CHOICE_VARIANTS = ['rock', 'paper', 'scissors']

    def __init__(self):
        self.user_name = self.ask_user_name()
        self.user_scores = self.get_user_scores()
        if self.user_scores is None:
            self.new_user = True
            self.user_scores = 0
        else:
            self.user_scores = int(self.user_scores)
        self.user_scores_current_session = 0
        random.seed()
        self.computer_choice = None
        self.user_choice = None

    def ask_user_choice(self):
        self.user_choice = input()
        while self.user_choice not in self.CHOICE_VARIANTS and self.user_choice not in ('!exit', '!rating'):
            print('Invalid input')
            self.user_choice = input()
        return self.user_choice

    @staticmethod
    def ask_user_name():
        user_name_ = input("Enter your name:")
        print('Hello, {}'.format(user_name_.capitalize()))
        return user_name_

    def get_user_scores(self):
        scores_in_file = None
        with open(self.RATING_FILE, 'r') as reader:
            for el in reader:
                if el.lower().startswith(self.user_name.lower()):
                    scores_in_file = el.replace('\n', '').split()[1]
        return scores_in_file

    def save_current_session_results(self):
        pass

    def ask_user_for_options_list(self):
        input_ = input("Enter custom options list: ")
        if input_ != '':
            self.CHOICE_VARIANTS = input_.split(',')
        print("Okay, let's start")

    def play_game(self):
        self.ask_user_for_options_list()
        self.ask_user_choice()
        self.change_computer_choice()
        while self.user_choice != '!exit':
            self.do_action()
            self.change_computer_choice()
            self.ask_user_choice()

        print('Bye!')
        self.save_current_session_results()

    def do_action(self):
        if self.user_choice == '!rating':
            self.print_rating()
        else:   
            self.game_result()

    def print_rating(self):
        if self.user_scores is not None:
            rating_to_print = self.user_scores + self.user_scores_current_session
            print("Your rating: {}".format(rating_to_print))
        else:
            print("Your rating: {}".format(self.user_scores_current_session))

    def change_computer_choice(self):
        self.computer_choice = random.choice(self.CHOICE_VARIANTS)

    def do_swap_list(self):
        index_of_user_choice = self.CHOICE_VARIANTS.index(self.user_choice)
        return_list = self.CHOICE_VARIANTS[index_of_user_choice + 1:] + self.CHOICE_VARIANTS[:index_of_user_choice]
        return return_list

    def do_win_list(self):
        prepare_list = self.do_swap_list()
        half_of_list_number = len(prepare_list) // 2
        return prepare_list[half_of_list_number:]

    def do_lose_list(self):
        prepare_list = self.do_swap_list()
        half_of_list_number = len(prepare_list) // 2
        return prepare_list[:half_of_list_number]

    def game_result(self):
        user_win_list = self.do_win_list()
        user_lose_list = self.do_lose_list()
        if self.computer_choice in user_win_list:  # user win
            self.user_scores_current_session += 100
            print('Well done. The computer chose {} and failed'.format(self.computer_choice))
        elif self.computer_choice in user_lose_list:  # user lost
            print('Sorry, but the computer chose {}'.format(self.computer_choice))
        else:  # draw
            self.user_scores_current_session += 50
            print('There is a draw ({})'.format(self.computer_choice))



my_game = RockPaperScissors()
my_game.play_game()
