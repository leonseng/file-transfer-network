import socket
import sys
import time


# DEFINE CONSTANTS
BUFFER_SIZE = 1024

# Check input arguments
if len(sys.argv) != 2:
    print("ERROR: Invalid input(s).")
    print("Usage:")
    print("\tpython server.py <server port>")
    sys.exit(1)

try:
    bindPort = int(sys.argv[1])
except ValueError:
    print("ERROR: server port must be between 1024 and 65535.")
    sys.exit(1)

# Define socket
serverSocket = socket.socket(type=socket.SOCK_DGRAM)
serverSocket.bind(("0.0.0.0", bindPort))

print("Server listening on {}:{}".format("0.0.0.0", bindPort))
    
# Start server code

"""
SAMPLE CODE

This sample code waits for a request packet from the client, and on receipt,
continuously sends out packets containing the string "hello"
"""
data, clientAddr = serverSocket.recvfrom(BUFFER_SIZE)
print("Received request from {}:\n{}".format(clientAddr, data))

serverSocket.settimeout(1)  # allows for CTRL+C break out
while True:
    serverSocket.sendto(b"hello", clientAddr)
    time.sleep(1)

"""
STUDENT CODE

Comment out sample code block above when running student's code 
"""
