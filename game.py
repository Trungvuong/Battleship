'''
This is the main python file that runs the Battleship game.
'''
from random import randint

board = []

for x in range(5):
    board.append(["O"] * 5)

def print_board(board):
    for row in board:
        print(" ".join(row))

print("Welcome to the game of Battleship!")
print_board(board)

def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0] - 1)

ship_row = random_row(board)
ship_col = random_col(board)
print(ship_row)
print(ship_col)

for turn in range(4):
    print("Turn ", turn + 1)
    guess_row = int(raw_input("Guess Row: "))
    guess_col = int(raw_input("Guess Column: "))
    break
if guess_row == ship_row and guess_col == ship_col:
    print("You sunk a battleship!")
else:
    if(guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
        print("Out of range!")
    elif(board[guess_row][guess_col] == "X"):
        print("This spot has already been guessed.")
    else:
        print("You missed the battleship!")
        board[guess_row][guess_col] == "X"
    turn + 1
    print_board(board)


