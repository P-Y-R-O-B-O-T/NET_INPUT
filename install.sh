#!/bin/bash

pip install cypher-protocol-P-Y-R-O-B-O-T
#pip install PyQt5

if [ -f "/usr/bin/netinp_server" ]; then
  sudo rm /usr/bin/netinp_server
fi

if [ -f "/usr/bin/netinp_client" ]; then
  sudo rm /usr/bin/netinp_client
fi

sudo chmod +x NET_INPUT/SERVER/server.py
sudo chmod +x NET_INPUT/CLIENT/client.py

sudo cp NET_INPUT/SERVER/server.py /usr/bin/netinp_server
sudo cp NET_INPUT/CLIENT/client.py /usr/bin/netinp_client
