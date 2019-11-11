#!/bin/bash
iperf -c 1.0.0.2 -p 5566 -u -t 10 -i 1 -b 100M