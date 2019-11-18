import socket
from random import randrange


class CustomSocket(socket.socket):
    """Socket that supports byte error on receiving packets

    """
    def __init__(self, bindPort, byteErrorRate=0, *args, **kwargs):
        # initializing socket and overriding unsupported functions
        super().__init__(*args, type=socket.SOCK_DGRAM, **kwargs)
        self.recv = CustomSocket._unsupported
        self.recvmsg = CustomSocket._unsupported
        self.recvmsg_into = CustomSocket._unsupported
        self.recvfrom_into = CustomSocket._unsupported
        self.recv_into = CustomSocket._unsupported

        self.byteErrorRate = byteErrorRate
        self.bind(("0.0.0.0", bindPort))
        self.settimeout(1)  # allows for CTRL+C break out

    def recvfrom(self, *args, **kwargs):
            while True:
                try:
                    data, addr = super().recvfrom(*args, **kwargs)
                    return self._jumbleData(data), addr
                except socket.timeout:
                    pass

    def _jumbleData(self, data):
        temp = bytearray(data)
        for i, _byte in enumerate(data):
            if (randrange(100) < self.byteErrorRate):
                newByte = randrange(256)
                temp[i] = newByte
        
        data = bytes(temp)
        return data
    
    @staticmethod
    def _unsupported(*args, **kwargs):
        print("WARN: Unsupported CustomSocket function.")
