from socket import *
import threading

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read().split("\n")

    # Send HTTP response headers
        connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n'.encode())

    # Send the content of the file
        connectionSocket.send(outputdata.encode())

    except IOError:
# Send a 404 response for file not found
        connectionSocket.send(b'HTTP/1.1 404 File Not Found\r\n\r\nFile not found.'.encode())

# Close the client socket
        connectionSocket.close()

# Create a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6788
# Bind the socket to a specific address and port
serverSocket.bind(('', serverPort))

# Listen for incoming connections
serverSocket.listen(5)

print('Ready to serve...')

while True:
# Accept a connection from a client
    connectionSocket, addr = serverSocket.accept()

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
    client_thread.start()