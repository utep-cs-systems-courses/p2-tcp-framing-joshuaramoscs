#! /usr/bin/env python3

import socket

class framedSocket:
    # Constructor
    def __init__(self, socket):
        self.sock = socket
        self.buff = "".encode()
        self.limit = 100

    # Send Message
    def send_msg(self, message):
        current_byte = 0
        # byte_array will look something like this: "5:hello"
        byte_array = str(len(message)).encode() + ':'.encode() + message.encode()
        sent_message = ""

        while len(byte_array) != 0: # Send in small pieces with buffer
            current_byte = self.sock.send(byte_array)
            sent_message += byte_array[:current_byte].decode()
            byte_array = byte_array[current_byte:]
        return new_message

    def recv_msg(self):
        # Recieve message
        if len(self.buff) == 0:     # buffer must be initially empty
            self.buff = self.sock.recv(self.limit).decode() # recv from socket and save it in buff
            if len(self.buff) == 0: # Recieved nothing. Should never happen.
                return ""
        else:                       # Buffer was not empty. Should never happen.
            return ""

        # Set initial buffer
        message_start = self.buff.index(':')
        message_len = int(self.buff[:message_start])
        self.buff = self.buff[message_start+1:]

        # Keep reading buffer
        message = ""
        while len(message) < message_len:
            if len(self.buff) ==0:    # if empty, recieve more
                self.buff = self.sock.recv(self.limit).decode()
            message += self.buff[0]   # read from buffer 1 char at a time
            self.buff = self.buff[1:] # remove the first character we just read
        return message
