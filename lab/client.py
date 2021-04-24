#! /usr/bin/env python3

import socket, sys, re, time, os
sys.path.append("../lib")       # for params
import params
from fileReader import my_fileReader
import framedSocket

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

if sys.argv[0] == "send":
    try:
        localFile = sys.argv[1]
        serverHost, remoteFile  = re.split(":", sys.argv[2])
        serverPort = 50001
    except:
        print("Invalid command. Try \"send [localFile] [serverHost]:[remoteFile]\"")
        sys.exit(1)

sock = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        sock = socket.socket(af, socktype, proto)
    except sock.error as msg:
        print(" error: %s" % msg)
        sock = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        sock.connect(sa)
    except sock.error as msg:
        print(" error: %s" % msg)
        sock.close()
        sock = None
        continue
    break

if sock is None:
    print('could not open socket')
    sys.exit(1)

framed_sock = framedSocket.framedSocket(sock)
sent = framed_sock.send_msg('send')
os.write(1, ("Sending " + sent + '\n').encode())

sent = framed_sock.send_msg(remoteFile)
os.write(1, ("Sending " + sent + '\n').encode())

response = framed_sock.recv_msg()
os.write(1, ("Receiving " + response + '\n').encode())

if response == "accept":
    print("Will now send file named " + localFile + '\n')
    data = my_fileReader(localFile)
    framed_sock.send_msg(data)
    os.write(1, "Sending {}\n".format(localFile).encode())

    response = framed_sock.recv_msg()
    os.write(1, "Receiving {} \n".format(response).encode())
    
sock.close()
