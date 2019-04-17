

import os
import socket
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

def main():
    # Creates authorization for users
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous('.', perm='elradfmwM')

    # Handle requests sent by the server
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner= "Connected"
    
    # Opens pipe and sockets
    pipe = os.popen("ip -4 route show default").read().split()
    sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sckt.connect((pipe[3], 0))
    address = sckt.getsockname()[0]

    # Creates server on port 3000 on localhost
    server = ThreadedFTPServer((address, 3000), handler)
    server.serve_forever()

#where the game takes place turn by turn
#commands to handle are place, shoot coord, update, end
#need to add game logic
#def game():
    

if __name__ == "__main__":
    main()
    #game()
                    


