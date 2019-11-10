import os
from sys import argv

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info


class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2, lossy=True ):
        switch = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        root = self.addNode('root', cpu=0.1, inNamespace=False)
        self.addLink(root, switch)

        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost(
                'h%s' % (h + 1),
                cpu=1/n,
                privateDirs = [('/tmp', '/home/leon/dev/filetransfer/hostdirs/h%s' % (h+1))]
            )

            # if lossy:
            #     # 10 Mbps, 5ms delay, 10% packet loss
            #     self.addLink(host, switch,
            #                  bw=10, delay='5ms', loss=10, use_htb=True)
            # else:
            #     # 10 Mbps, 5ms delay, no packet loss
            #     self.addLink(host, switch,
            #                  bw=10, delay='5ms', loss=0, use_htb=True)

            self.addLink(host, switch)

            self.addLink(host, switch2,
                             bw=100, delay='5ms', loss=10, use_htb=True, params1={'ip':'100.0.0.%d/24' % (h+1)} )

def perfTest( lossy=True ):
    "Create network and run simple performance test"
    topo = SingleSwitchTopo( n=2, lossy=lossy )
    net = Mininet( topo=topo,
                   host=CPULimitedHost, link=TCLink,
                   autoStaticArp=True )
        
    net.start()
    
    root = net.getNodeByName('root')
    root.setIP("1.0.0.10/24")
    
    for h in range(2):
        hostName = 'h{}'.format(h + 1)
        host = net.getNodeByName(hostName)
        host.setIP('1.0.0.{}/24'.format(h + 1))
        host.cmd("/usr/sbin/sshd &")
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    os.system("sudo mn -c")
    setLogLevel( 'info' )
    # Prevent test_simpleperf from failing due to packet loss
    perfTest( lossy=( 'testmode' not in argv ) )