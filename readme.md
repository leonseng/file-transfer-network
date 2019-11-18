# Topology
This is a 2 hosts, 2 switches Mininet topology. However, only 1 switch, s1 carries data plane traffic

    server --- switch s1 --- client

 An additional switch, s0 has been configured to enable management access to the hosts via SSH. Link options such as bandwitch, delay and packet loss rate can be configured in `settings.json`

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

To open a shell to either hosts, use `xterm` in the mininet prompt
```
mininet> xterm server
OR
mininet> xterm client
```

Each host has its own `/data` directory mapped to a local `host-dirs/<host-type>` directory. The client has an additional *private* directory `/download`

To run the server/client code, run the following command in the respective shell
### Server
```
server> cd /data
server> python server.py <server-port>
```

### Client
```
client> cd /data
client> python client.py <server-ip> <server-port> <filename>
```