import json
import os
from sys import argv

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info, error

JUMPHOST = "jumphost"
SERVER = "server"
CLIENT = "client"

SSHD_CMD = "/usr/sbin/sshd"

# load settings
with open("settings.json") as f:
    SETTINGS = json.load(f)

class FileTransferTopo( Topo ):
    "Single switch connected to n hosts."
    def build(self):

        switches = {}
            
        def addHost(hostName, cpu, privateDirs=[]):
            hostSettings = SETTINGS["hosts"][hostName]
            host = self.addHost(
                hostName, 
                cpu=cpu, 
                privateDirs=privateDirs, 
                inNamespace=hostSettings.get("inNamespace", True)
            )

            # link host interfaces to switches based on network they are in
            for intf in hostSettings["interfaces"]:
                # determine which switch to connect the interface to
                intfNetwork = intf["network"]
                if intfNetwork not in switches:
                    # create new switch for network if not already present
                    switches[intfNetwork] = self.addSwitch("s" + str(len(switches)))

                self.addLink(host, switches[intfNetwork], **intf.get("linkOpt", {}))
                  
        addHost(JUMPHOST, 0.1)
        addHost(SERVER, 0.4, [("/tmp", "./hostdirs/server")])
        addHost(CLIENT, 0.4, [("/tmp", "./hostdirs/client")])

def setupNetwork( lossy=True ):
    "Create network and configure interface IPs"
    net = Mininet( 
        topo=FileTransferTopo(),
        host=CPULimitedHost, 
        link=TCLink,
        autoStaticArp=True
    )        
    net.start()
    
    def configureHost(hostName):
        host = net.getNodeByName(hostName)
        hostSettings = SETTINGS["hosts"][hostName]

        # configure interface IP
        for i, intf in enumerate(hostSettings["interfaces"]):
            host.setIP(
                intf["ip"], 
                intf["prefixLen"], 
                "{}-eth{}".format(hostName, i)
            )

        # start SSH server
        if hostSettings.get("inNamespace", True):
            info("Enabling SSHD on {}\n".format(hostName))
            host.cmd(SSHD_CMD + " -D -o UseDNS=no -u0 &")

    configureHost(JUMPHOST)
    configureHost(SERVER)
    configureHost(CLIENT)
    
    try:
        CLI(net)
    finally:
        # clean up
        for host in net.hosts:
            host.cmd('kill %' + SSHD_CMD)

        net.stop()
        # os.system("sudo mn -c")

if __name__ == "__main__":
    os.system("sudo mn -c")
    setLogLevel("info")    
    setupNetwork()