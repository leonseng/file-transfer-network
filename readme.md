# Topology
This is a 2 hosts, 1 switch topology.

    server --- switch s1 --- client

An additional switch s0 has been configured to enable management access to the hosts via SSH. Link options such as bandwitch, delay and packet loss rate can be configured in `settings.json`

# Instructions
To start the topology, run (note: as `sudo`) the following command:
`sudo python simple_topo.py`

## IPerf test
### Server
`/tmp/iperf-server.sh`

### Client
`/tmp/iperf-client.sh`