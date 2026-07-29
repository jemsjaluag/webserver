#Import socket module

from socket import *
import sys, threading

import socket # Alternative (better) syntax

##### create class for threading
class ClientThread(threading.Thread):
    def __init__(self, clientSocket, clientAddress):
        threading.Thread.__init__(self)
        self.connectionSocket = clientSocket
        print("\nNew connection added: ", clientAddress)

    ### override the Thread's run method to run our code
    def run(self):
        try:

    # Receives the request message from the client
            self.message = self.connectionSocket.recv(1024).decode()
            print(f'Message is: {self.message}')

    # Extract the path of the requested object from the message
    # The path is the second part of HTTP header, identified by [1]
            self.filename = self.message.split()[1]
            print(f'File name is: {self.filename}')

    # Because the extracted path of the HTTP request includes
    # a character '/', we read the path from the second character
            self.f = open(self.filename[1:])

    # Store the entire contenet of the requested file in a temporary buffer
            self.outputdata = self.f.read().split("\n")
            print(f"OUTPUT DATA: {self.outputdata}")

    # Send the HTTP response header line to the connection socket
            self.connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

    # Send the content of the requested file to the connection socket
            for i in range(0, len(self.outputdata)):
                self.connectionSocket.send(self.outputdata[i].encode())
                self.connectionSocket.send("\r\n".encode())

    # Close the client connection socket
            self.f.close()                   ## close file as well
            self.connectionSocket.close()

        except IOError:
            # Send HTTP response message for file not found
            self.connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            self.connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    # Close the client connection socket
            self.connectionSocket.close()
            sys.exit()
        


# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
# serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Alternative (better) syntax

# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))
# or
# serverSocket.bind((gethostname(), serverPort))
# serverSocket.bind((socket.gethostname(), serverPort)) # Alternative (better) syntax

while True:
# Listen to at most 1 connection at a time
    print('Ready to serve...')
    serverSocket.listen(1)
    clientSocket, clientAddress = serverSocket.accept()
    # create new thread using the class made above
    newThread = ClientThread(clientSocket, clientAddress)
    # start the thread
    newThread.start()

# Server should be up and running and listening to the incoming connections
#sys.exit()