import socket
import sys


def http_client(server_host, server_port, filename):

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        # Connect to the server
        client_socket.connect((server_host, server_port))

        # Send the HTTP GET request
        request = f"GET {filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"

        client_socket.sendall(request.encode())

        # Receive and display the server response
        # header
        response = client_socket.recv(4096).decode()
        print(response)

        # contents
        contents = client_socket.recv(4096).decode()
        print(contents)


    except socket.error as e:
        print(f"Error: {e}")

    finally:

        # Close the socket
        client_socket.close()


# Check if the script is run with the correct number of command line arguments

if len(sys.argv) != 4:
    print("Usage: python client.py server_host server_port filename")

else:
    # Parse the command line arguments
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    # Call the HTTP client function
    http_client(server_host, server_port, filename)