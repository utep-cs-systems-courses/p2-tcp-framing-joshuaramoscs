#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params, framedSocket
import serverThread

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((listenAddr, listenPort))
sock.listen(1)              # allow only one outstanding request
# sock is a factory for connected sockets

while True:
    connectedSock, address = sock.accept() # wait until incoming connection request (and accept it)
    serverThread.serverThread(connectedSock, address).start()
