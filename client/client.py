import os, socket
from ftplib import FTP

ftp = FTP('')

connection = False

def start(ip, port):
    ftp.connect(ip, int(port))

    #client chooses what player
    print('Choose p1 or p2')
    player = input('>>> ')

    #login as player
    ftp.login(player)
    print('Connected successfully...')
    connection = True

def game():
    print('Welcome to BattleShip!')

    print('Enter Number of Ships [1-10]!')
    num = input('>>> ')

    #send commands to place ships
    ftp.sendcmd(" ".join(['place', num])

    while(true):
        print('Choose where to shoot [a1, b1, c1, ect...] or QUIT')

        coord = input('>>> ')

        #sends commands of where to shoot
        ftp.sendcmd(" ".join(['shoot', coord]))

        #send command to update board
        ftp.sendcmd('update')

        #send end turn command
        ftp.sendcmd('end')

        #busy wait for other player to play

        #update board
        ftp.sendcmd('update')

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
    if 'QUIT' in response:
        ftp.quit()
        print('Disconnecting from server...')
