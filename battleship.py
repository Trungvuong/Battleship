'''
This program runs an instance of the classic Battleship game in 
Python3. The prompt initially asks the user for their classification:
either host or client. Then the names of the two will be asked and then
the two players will be able to play each other in the game Battleship.
The player's pieces will be randomized and each user gets a turn to 
guess the ship's locations. A simple implementation of Battleship.
Enjoy.

@author Trung-Vuong Pham, Ryan Eisenbarth, and Kevin Holkeboer
@version 1.0
'''
# required imports for the program
import argparse
import os
import platform
import random
import socket
import sys
from pickle import dumps, loads

# This is the player class
class Player:
    ships_len = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
    
    # This was the way we wanted to indicate the statuses of the ships
    sym_ship = '●'
    sym_hit = 'x'
    sym_miss = 'o'
    sym_destroyed = '*'
    sym_empty = '·'
    
    # Constructor method for our class
    def __init__(self, name):
        self.name = name
        self.fleet = {}
        self.game_board = self.__create_empty_board()
        self.guess_board = self.__create_empty_board()
        self.__position_ships_on_board()
        self.my_ships_destroyed = 0
        self.opponent_ships_destroyed = 0
    
    # This creates an empty board 
    @staticmethod
    def __create_empty_board():
        temp = {}
        for x in 'ABCDEFGHIJ':
            for y in range(1, 11):
                temp[x, y] = __class__.sym_empty
        return temp
    
    # Helper method to clear screen
    @staticmethod
    def clear():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    
    # Method to print the board
    def print_board(self, me, opponent):
        self.clear()
        for i in (self.game_board, self.guess_board):
            if i == self.game_board:
                print("{}\n{}".format(me, '-' * len(self.name)))
            else:
                print("{}\n{}".format(opponent, '-' * len(opponent)))
            
            # This approach was the way we were able to get the board 
            # to print how we wanted it to print
            print("""  1 2 3 4 5 6 7 8 9 10
A {} {} {} {} {} {} {} {} {} {}
B {} {} {} {} {} {} {} {} {} {}
C {} {} {} {} {} {} {} {} {} {}
D {} {} {} {} {} {} {} {} {} {}
E {} {} {} {} {} {} {} {} {} {}
F {} {} {} {} {} {} {} {} {} {}
G {} {} {} {} {} {} {} {} {} {}
H {} {} {} {} {} {} {} {} {} {}
I {} {} {} {} {} {} {} {} {} {}
J {} {} {} {} {} {} {} {} {} {}
""".format(
                i['A', 1], i['A', 2], i['A', 3], i['A', 4], i['A', 5],
                i['A', 6], i['A', 7], i['A', 8], i['A', 9], i['A', 10],
                i['B', 1], i['B', 2], i['B', 3], i['B', 4], i['B', 5],
                i['B', 6], i['B', 7], i['B', 8], i['B', 9], i['B', 10],
                i['C', 1], i['C', 2], i['C', 3], i['C', 4], i['C', 5],
                i['C', 6], i['C', 7], i['C', 8], i['C', 9], i['C', 10],
                i['D', 1], i['D', 2], i['D', 3], i['D', 4], i['D', 5],
                i['D', 6], i['D', 7], i['D', 8], i['D', 9], i['D', 10],
                i['E', 1], i['E', 2], i['E', 3], i['E', 4], i['E', 5],
                i['E', 6], i['E', 7], i['E', 8], i['E', 9], i['E', 10],
                i['F', 1], i['F', 2], i['F', 3], i['F', 4], i['F', 5],
                i['F', 6], i['F', 7], i['F', 8], i['F', 9], i['F', 10],
                i['G', 1], i['G', 2], i['G', 3], i['G', 4], i['G', 5],
                i['G', 6], i['G', 7], i['G', 8], i['G', 9], i['G', 10],
                i['H', 1], i['H', 2], i['H', 3], i['H', 4], i['H', 5],
                i['H', 6], i['H', 7], i['H', 8], i['H', 9], i['H', 10],
                i['I', 1], i['I', 2], i['I', 3], i['I', 4], i['I', 5],
                i['I', 6], i['I', 7], i['I', 8], i['I', 9], i['I', 10],
                i['J', 1], i['J', 2], i['J', 3], i['J', 4], i['J', 5],
                i['J', 6], i['J', 7], i['J', 8], i['J', 9], i['J', 10])
            )

    # This method creates the positions on the board
    # Ships are placed randomly and should never touch each other
    def __position_ships_on_board(self):
        for ship_num, ship_len in enumerate(self.ships_len, 1):
            self.fleet[ship_num] = {}
            while True:
                # This was how we randomized the board so the players don't have to physically 
                # choose spots for ships.
                direction = random.choice([(0, 1), (1, 0)])  # horizontal→(0, 1) vertical↓(1, 0)
                row = random.choice('ABCDEFGHIJ')  # choose row
                col = random.choice(range(1, 11))  # choose column
                temp = {} # This creates a temporary board
                for part in range(ship_len):
                    for a, b in [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        try:
                            if self.game_board[chr(ord(row) + part * direction[0] + a), col + part * direction[1] + b] \
                                    != __class__.sym_empty:
                                break
                        # Exception
                        except KeyError:
                            if a == 0 and b == 0:
                                break
                    else:
                        temp[(chr(ord(row) + part * direction[0]), col + part * direction[1])] = False
                        continue
                    break
                else:
                    self.fleet[ship_num] = temp
                    for part in self.fleet[ship_num]:
                        self.game_board[part] = __class__.sym_ship
                    break

    # Method to retrieve a user's guess
    def get_user_guess(self):
        while True:  # Loop until proper input is received 
            try:
                flush_input()  # clear all keystrokes made by user 
                user = input("{}, Select Row and column (e.g. A1): ".format(self.name))  # Get row and column
                row = user[0].upper()  # Verifies letter is uppercase in guess
                col = int(user[1:])  # Verifies the digits after letter are numbers
                if row in 'ABCDEFGHIJ' and col in range(1, 11):  # Checks for range in row and columns
                    if self.guess_board[row, col] == __class__.sym_empty:  # Check for a guess on an empty cell
                        return row, col  # return the row and col
            # Exceptions to watch out for 
            except (ValueError, IndexError):
                pass
            except KeyboardInterrupt:
                print("\nBye!")
                sys.exit(0)
    
    # Method to check if a guess hit
    def check_if_hit(self, row, col):
        if self.game_board[row, col] == __class__.sym_ship:
            return True
        return False
    
    # Method to create marks on the board
    @staticmethod
    def mark_on_board(row, col, hit, board_type):
        if hit:
            board_type[row, col] = __class__.sym_hit
        else:
            board_type[row, col] = __class__.sym_miss

    # Method to mark on a fleet that was guessed
    def mark_on_fleet(self, row, col):
        for ship in self.fleet:
            if (row, col) in self.fleet[ship]:
                self.fleet[ship][row, col] = True
                return ship

    # Method to check for destroyed ships
    def check_if_ship_destroyed(self, ship):
        for part in self.fleet[ship]:  # check if all parts of the ship got hit
            if self.fleet[ship][part] is False:  # if at least one part wasn't hit return false
                return False
        else:  # if all parts of ship got hit
            return True
    
    # Method to mark the destroyed ships
    @staticmethod
    def mark_destroyed_ship_on_board(ship, board_type):
        for part in ship:
            board_type[part] = __class__.sym_destroyed
            for a, b in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                try:
                    if board_type[chr(ord(part[0]) + a), part[1] + b] == __class__.sym_empty:
                        board_type[chr(ord(part[0]) + a), part[1] + b] = __class__.sym_empty
                except KeyError:
                    pass

# Method to retrieve IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# System to flush the input
def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

# Main method for our program
def main():
    try:
        port = 3000

        # parsing arguments #
        parser = argparse.ArgumentParser()
        g = parser.add_mutually_exclusive_group()
        g.add_argument('-c', dest='server_ip', help='Run as Client') # Client
        g.add_argument('-s', dest='server', action='store_true', help='Run as Server') # Server
        args = parser.parse_args()
        if args.server is False and args.server_ip is None:
            parser.error("At least one flag is required")

        # This is the socket connection between the server and client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if args.server:
            s.bind(("0.0.0.0", port)) # binds
            s.listen(1)
            print('Waiting for opponent to join me at {}:{}'.format(get_ip_address(), port))
            s, addr = s.accept()
            print('Received connection: {}:{}'.format(addr[0], addr[1]))
            my_turn = False
        else:
            s.connect((args.server_ip, port))
            my_turn = True

        # Asks and send player's names
        my_name = input("Enter your name: ")  # Gets my name
        s.send(dumps(my_name))  # Send name to opponent
        opponent_name = loads(s.recv(1024))  # Receive opposing player's name
        p = Player(my_name)  # Creates my player
        p.print_board(my_name, opponent_name)  # print game board

        # Game logic
        while True:  
            if my_turn:  # My turn
                row, col = p.get_user_guess()  # Receives guess
                s.send(dumps((row, col)))  # Send guess
                hit = loads(s.recv(1024))  # Opponent determines if it is a hit or miss
                if hit: 
                    message = "You guessed {}{} - HIT".format(row, col)
                    p.mark_on_board(row, col, True, p.guess_board)  # Mark hit on my guess board
                    ship_destroyed = (loads(s.recv(1024)))  # Get opponent notification if I destroyed a ship
                    if ship_destroyed:  # If I destroyed opponent's ship
                        p.mark_destroyed_ship_on_board(ship_destroyed, p.guess_board)  # Reveal ship on my guess board
                        p.opponent_ships_destroyed += 1  # Increment opponent ships destroyed
                        if p.opponent_ships_destroyed == len(p.ships_len):  # If all opponent's ships are destroyed
                            break  # stop game main loop
                else:  # If I missed
                    message = "You guessed {}{} - MISS".format(row, col)
                    p.mark_on_board(row, col, False, p.guess_board)  # Mark a miss on my guess board
                my_turn = False  # Switch turns
            else:  # If its opponent's turn
                print("Waiting for {} to send his guess".format(opponent_name))  
                row, col = loads(s.recv(1024))  # Receive guessed row and column from opponent
                if p.check_if_hit(row, col):  # If opponent hit one of my ships
                    msg = "{} guessed {}{} - HIT".format(opponent_name, row, col)
                    s.send(dumps(True))  # Tells opponent they hit one of my ships
                    p.mark_on_board(row, col, True, p.game_board)  # Mark hit on my game board
                    ship_that_got_hit = p.mark_on_fleet(row, col)  # Checks which of my ships got hit
                    if p.check_if_ship_destroyed(ship_that_got_hit):  # If the ship that got hit was destroyed
                        s.send(dumps(p.fleet[ship_that_got_hit]))  # Notify coordinates of destroyed ship to opponent
                        p.mark_destroyed_ship_on_board(p.fleet[ship_that_got_hit],
                                                       p.game_board)  # Reveal ship on game board
                        p.my_ships_destroyed += 1  # Count ships destroyed
                        if p.my_ships_destroyed == len(p.ships_len):  # If all my ships are destroyed
                            break  # Stop game main loop
                    else:  # If the ship that got hit wasn't destroyed
                        s.send(dumps(False))  # Notify opponent that the hit didn't destroy a ship
                else:  # If opponent misses
                    message = "{} guessed {}{} - MISS".format(opponent_name, row, col)
                    s.send(dumps(False))  # Notify opponent that he missed
                    p.mark_on_board(row, col, False, p.game_board)  # Mark the miss on my game board
                my_turn = True  # Switch turns
            p.print_board(my_name, opponent_name)  # Print board after each turn
            print(message)

        # This portion is where the winner is declared
        p.print_board(my_name, opponent_name)  # Prints final look of game board
        if p.my_ships_destroyed > p.opponent_ships_destroyed:
            print("{} is the winner!".format(opponent_name))  # Opponent is the winner
        else:
            print("{} is the winner!".format(my_name))  # I am the winner
    
    # Various exceptions for the program we could potentially encounter
    except KeyboardInterrupt:
        print("\nBye!")
    except (EOFError, ConnectionAbortedError, ConnectionResetError):
        print("\n Opponent has disconnected")
    except ConnectionRefusedError:
        print("Server never started or there is a network problem")

if __name__ == '__main__':
    main()
