#! /usr/bin/env python3

import socket

class framedMsg:
    def __init__(self):
        
        self.buff = "".encode()
        self.limit = 100

    def send_msg(self, msg):
        byte_arr = str(len(msg)).encode() + ':'.encode() + msg.encode()
        new_msg = ""

        while len(byte_arr) != 0:
            last_byte = self.sock.send(byte_arr)
            new_msg += byte_arr[:last_byte].decode()
            byte_arr = byte_arr[last_byte:]
        return new_msg

    def recv_msg(self):
        if len(self.buff) == 0:
            self.buff = self.sock.recv(self.limit).decode()
            if len(self.buff) == 0:
                return ""
        msg_start = self.buff.index(':')
        msg_len = int(self.buff[:msg_start])
        self.buff = self.buff[msg_start+1:]

        msg = ""
        while len(msg) != msg_len:
            if len(self.buff) ==0:
                self.buff = self.sock.recv(self.limit).decode()
            msg += self.buff[0]
            self.buff = self.buff[1:]
        return msg
