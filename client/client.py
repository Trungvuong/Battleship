import os, socket
from ftplib import FTP

ftp = FTP('')

connection = False

def start(ip, port):
    ftp.connect(ip, int(port))
    ftp.login()
    print('Connected successfully...')
    connection = True

def main():
    global ftp
    response = input('>>> ')
    connection = False

    if 'CONNECT' in response:
        argument = response.split()
        if len(argument) == 3:
            start(argument[1], argument[2])
            argument = []
            main()
        else:
            print("CONNECT needs an IP address and port number!\n ")
            main()
        elif 'QUIT' in response:
            ftp.quit()
            print('Disconnecting from server...')
