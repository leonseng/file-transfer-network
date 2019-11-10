from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info

from sys import argv

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2, lossy=True ):
        switch = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')



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

            self.addLink(host, switch,
                             bw=100, delay='5ms', loss=0, use_htb=True)

            self.addLink(host, switch2,
                             bw=100, delay='5ms', loss=10, use_htb=True, params1={'ip':'10.0.0.%d/24' % (h+1)} )

def perfTest( lossy=True ):
    "Create network and run simple performance test"
    topo = SingleSwitchTopo( n=2, lossy=lossy )
    net = Mininet( topo=topo,
                   host=CPULimitedHost, link=TCLink,
                   autoStaticArp=True )    
    
    net.start()

    # get cli instance
    cli = CLI(net, script='null-script')

    # info( "Dumping host connections\n" )
    # dumpNodeConnections(net.hosts)
    # info( "Testing bandwidth between h1 and h2\n" )
    # h1, h2 = net.getNodeByName('h1', 'h2')
    # net.iperf( ( h1, h2 ), l4Type='UDP' , udpBw = '10M', seconds= 10)    
        
    h1, h2 = net.getNodeByName('h1', 'h2')
    h1.setIP('1.0.0.2/24')
    h1.cmd("cd /tmp")
    h2.setIP('1.0.0.3/24')
    h2.cmd("cd /tmp")    
    
    CLI.do_xterm(cli, "h1")
    CLI.do_xterm(cli, "h2")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    # Prevent test_simpleperf from failing due to packet loss
    perfTest( lossy=( 'testmode' not in argv ) )