#!/bin/bash
iperf -c 100.0.0.1 -p 5566 -u -t 10 -i 1 -b 100M