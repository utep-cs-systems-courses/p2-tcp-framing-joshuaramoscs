import os, sys, socket, time
from threading import Thread, enumerate
import framedSocket

threadNum = 0 # global thread count
lock = threading.Lock()

class serverThread(Thread):
    def __init__(self, connectedSock, addr):
        global threadNum
        Thread.__init__(self, name = "Thread-%d" % threadNum)
        threadNum += 1
        self.connectedSock = connectedSock
        self.addr = addr

    def run(self):
        print("Working in Thread-%d" % threadNum)
        framed_sock = framedSocket.framedSocket(self.connectedSock)

        request = framed_sock.recv_msg()
        os.write(1, "Recieving: {}\n".format(request).encode())

        if request == "send":
            fileName = framed_sock.recv_msg()
            os.write(1, "Receiving {}\n".format(fileName).encode())

            path = "./server/"+fileName

            
            if os.path.isfile(path):
                sent = framed_sock.send_msg("This file aready exists.")
                os.write(1, "Sending {}\n".format(sent).encode())

            else:
                os.write(1, ("Sending: " + framed_sock.send_msg("accept") + "\n").encode())
                fd = os.open("./server/"+fileName, os.O_CREAT | os.O_WRONLY)
                os.write(fd, (framed_sock.recv_msg()).encode())
                os.close(fd)
                os.write(1, "File {} created.\n".format(fileName).encode())
        else:
            os.write(1, "Inconplete request".encode())
        self.connectedSock.shutdown(socket.SHUT_WR)
