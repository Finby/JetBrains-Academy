X_SIGN = 'X'
O_SIGN = 'O'
EMPTY_FIELD = ' '

def make_list(field_string):
    field = []
    field_string = field_string.replace('_', EMPTY_FIELD)
    for i in range(3):
        field.append([char for char in field_string[9 - 3 * (i + 1):9 - 3 * i]])
    return field

def draw_field():
    print("-" * 9)
    for i in range(len(matrix) - 1, -1, -1):
        print("|", " ".join(matrix[i]), "|")
    print("-" * 9)


def is_next_step():
    return bool([field for rows in matrix for field in rows if field == EMPTY_FIELD])


def is_full_row(el):
    return bool([row for row in matrix if row == [el] * 3])


def is_full_column(el):
    transpose_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return is_full_row(el)


def is_full_diagonal(el):
    return matrix[0][0] == matrix[1][1] == matrix[2][2] == el \
           or matrix[0][2] == matrix[1][1] == matrix[2][0] == el


def is_win(el):
    return any((is_full_row(el), is_full_column(el), is_full_diagonal(el)))


def difference_number(el_1, el_2):
    el_1_number = len([x for row in matrix for x in row if x == el_1])
    el_2_number = len([x for row in matrix for x in row if x == el_2])
    return abs(el_1_number - el_2_number)


def game_status():
    status = "Game not finished"
    if is_win(O_SIGN) and is_win(X_SIGN) or difference_number(O_SIGN, X_SIGN) >= 2:
        status = "Impossible"
    elif is_win(O_SIGN):
        status = 'O wins'
    elif is_win(X_SIGN):
        status = 'X wins'
    elif not is_next_step():
        status = "Draw"
    return status


def is_valid_coordinates(move_coordinates):
    valid = True
    try:
        x, y = move_coordinates.split()
        x = int(x)
        y = int(y)
    except:
        print("You should enter numbers!")
        return False
    if valid and (x not in (1, 2, 3) or y not in (1, 2, 3)):
        print("Coordinates should be from 1 to 3!")
        valid = False
    elif matrix[y - 1][x - 1] != ' ':
        print("This cell is occupied! Choose another one!")
        valid = False
    return valid


def make_move(x, y, el):
    matrix[y - 1][x - 1] = el


def get_correct_coordinates():
    move_coordinates = input("Enter the coordinates: ")
    while not is_valid_coordinates(move_coordinates):
        move_coordinates = input("Enter the coordinates: ")
    return move_coordinates.split()

matrix = make_list('_' * 9)
draw_field()

current_sign = X_SIGN
while game_status() == "Game not finished":
    x, y = get_correct_coordinates()
    make_move(int(x), int(y), current_sign)
    current_sign = X_SIGN if current_sign == O_SIGN else O_SIGN
    draw_field()

print(game_status())


# print(game_status())
# print(is_full_row(field_list, O_SIGN))
# print(is_full_column(field_list, O_SIGN))
# print(is_full_column(field_list, X_SIGN))
