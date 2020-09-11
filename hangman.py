import random
from string import ascii_lowercase


class HangMan:
    def __init__(self, word_list, number_of_tries):
        print('H A N G M A N')
        # random.seed()
        self.word_to_guess = random.choice(word_list)
        self.left_tries = number_of_tries
        self.word_current_status = ['-'] * len(self.word_to_guess)
        self.used_letters = []

    def __print_current_status__(self):
        print(''.join(self.word_current_status))

    def is_word_guessed(self):
        return self.word_to_guess == ''.join(self.word_current_status)

    def the_game(self):
        # while self.left_tries and (not self.is_word_guessed() or self.tries_to_do > 0):
        while self.left_tries and not self.is_word_guessed():
            print()
            self.__print_current_status__()
            letter_ = input('Input a letter: ')
            if len(letter_) != 1:
                print('You should input a single letter')
            elif letter_ not in ascii_lowercase:
                print('It is not an ASCII lowercase letter')
            elif letter_ in self.used_letters:
                print('You already typed this letter')
            elif letter_ not in self.word_to_guess or letter_ is None:
                if self.left_tries:
                    print('No such letter in the word')
                self.left_tries -= 1
            else:
                for i in range(len(self.word_to_guess)):
                    if self.word_to_guess[i] == letter_:
                        self.word_current_status[i] = letter_
            self.used_letters.append(letter_)

        if self.left_tries > 0:
            print('You guessed the word {}!\nYou survived!'.format(self.word_to_guess))
        else:
            print('You are hanged!')
        # print("""Thanks for playing! \nWe'll see how well you did in the next stage""")

    def game_menu(self):
        while True:
            user_answer = input('Type "play" to play the game, "exit" to quit:')
            if user_answer == 'exit':
                break
            else:
                self.the_game()


start_word_list = ('python', 'java', 'kotlin', 'javascript')
game_tries = 8
mygame = HangMan(start_word_list, game_tries)
mygame.game_menu()
