import os, socket
from ftplib import FTP

ftp = FTP('')

connection = False

def start(ip, port):
    ftp.connect(ip, int(port))
    ftp.login()
    print('Connected successfully...')
    connection = True

def game():
    print('Welcome to BattleShip!')

    int player = 0

    #receives what player it is

    print('Place your Ships!')

    #send commands to place ships

    while(true):
        print('Choose where to shoot or QUIT')

        #sends commands of where to shoot

        #update board

        #wait for other player

        #update board

def main():
    global ftp
    response = input('>>> ')
    connection = False

    if 'CONNECT' in response:
        argument = response.split()
        if len(argument) == 3:
            start(argument[1], argument[2])
            argument = []
            game()
        else:
            print("CONNECT needs an IP address and port number!\n ")
            main()
        elif 'QUIT' in response:
            ftp.quit()
            print('Disconnecting from server...')
