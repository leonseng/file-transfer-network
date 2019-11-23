import sys

from DefectiveSocket import DefectiveSocket

# DEFINE CONSTANTS
BYTE_ERROR_RATE = 5  # in percentage
BUFFER_SIZE = 1024

# Check input arguments
if len(sys.argv) != 4:
    print("ERROR: Invalid input(s).")
    print("Usage:")
    print("\tpython client.py <server IP> <server port> <filename>")
    sys.exit(1)

serverIp = sys.argv[1]

try:
    serverPort = int(sys.argv[2])
except ValueError:
    print("ERROR: server port must be between 1024 and 65535.")
    sys.exit(1)

fileName = sys.argv[3]
serverAddr = (serverIp, serverPort)

# Define socket
clientSocket = DefectiveSocket(0, BYTE_ERROR_RATE)

# Start client code
# SAMPLE CODE - comment out section below when running student's code

print("Initiating request to server {}:{}".format(*serverAddr))
clientSocket.sendto(b"hello", serverAddr)
clientSocket.settimeout(1)  # allows for CTRL+C break out
while True:
    data, addr = clientSocket.recvfrom(BUFFER_SIZE)
    print("Rx: {} from {}".format(data, addr))