# Topology
This is a 2 hosts, 1 switch Mininet topology.

    server --- switch s1 --- client

# Installation on Ubuntu
To support Python 3.x, the latest version of Mininet (from Master branch) is required.

## Mininet
1. Set Python 3 as the default Python binary

    ```
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
    ```

1. Clone Mininet master branch

    ```
    cd ~
    git clone git://github.com/mininet/mininet
    ```

1. Install Mininet - this will take a while

    ```
    ~/mininet/util/install.sh -a
    ```

1. Verify installation - should expect an output of 0 

    ```
    python -c "from mininet.topo import Topo" && echo $?
    ```

# Usage
To start the topology, run (note: as `sudo`) the following command:
`sudo python filetransfer_network.py`

The server has the IP `100.0.0.1/24`, whereas the client has the IP `100.0.0.2/24`. The client is also configured with a *private* directory `/ftdownload`

To open a shell to either hosts, use `xterm` in the mininet prompt
```
mininet> xterm server
OR
mininet> xterm client
```

To run the server/client code, run the following command in the respective shell
### Server
```
server> python server.py <server-port>
```

### Client
```
client> python client.py <server-ip> <server-port> <filename>
```