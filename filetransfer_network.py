import os

from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import Controller, CPULimitedHost

def FileTransferNetwork():
    "Create an empty network and add nodes to it."

    net = Mininet(
        host=CPULimitedHost, 
        link=TCLink,
        autoStaticArp=True
    )

    info( '*** Adding controller\n' )
    # turns OVS switch into an Ethernet bridge/learning bridge
    net.addController('c0')

    info( '*** Adding hosts\n' )
    server = net.addHost('server', ip='100.0.0.1/24', privateDirs=[("/data", "./host-dirs/server")])
    client = net.addHost('client', ip='100.0.0.2/24', privateDirs=[("/data", "./host-dirs/client"), "/download"])

    info( '*** Adding switches\n' )
    s1 = net.addSwitch('s1')

    info( '*** Creating links\n' )
    # We add bidirectional links with bandwidth, delay and loss
    # characteristics, with a maximum queue size of 1000 packets.
    # bw is expressed as a number in Mbit.
    # delay is expressed as a string with units in place
    # (e.g. '5ms', '100us', '1s')
    # loss is expressed as a percentage (between 0 and 100), and
    # max_queue_size is expressed in packets.
    net.addLink(server, s1, bw=10, delay='5ms', loss=0, use_htb=True)
    net.addLink(client, s1, bw=10, delay='5ms', loss=0, use_htb=True)

    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI(net)

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    os.system("sudo mn -c")
    setLogLevel( 'info' )
    FileTransferNetwork()