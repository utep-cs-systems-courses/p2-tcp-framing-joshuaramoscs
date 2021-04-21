#! /usr/bin/env python3

import os

ibuf = ""      # Input buffer
sbuf = ""      # String buffer
sbufLength = 0 # String buffer length
currChar = 0   # Index of current char in sbuf

def my_getChar(fd):
    global ibuf
    global sbuf
    global sbufLength
    global currChar
    
    if currChar == sbufLength: # If we reached the end of sbuf, get a new line and reset values
        ibuf = os.read(fd, 100)
        sbuf = ibuf.decode()
        sbufLength = len(sbuf)
        currChar = 0
        if sbufLength == 0:    # If we reached the end of the input, return nothing
            return ''
    
    char = sbuf[currChar]
    currChar += 1
    return char

def my_readLine(fd):
    char = my_getChar(fd)
    line = ""
    
    while char != '\n':     # While char is not equal to new line, keep getting chars for line
        line += char
        char = my_getChar(fd)
        if char == '':      # If char is empty, then we reached EOF; retun
            return line
    line+= '\n'             # If a new line was found, then return the line with a new line char
    return line

def my_fileReader(fileName):
    fd = os.open(fileName, os.O_RDONLY)
    fileContent = ""
    line = my_readLine(fd)
    while line != "":
        fileContent += line
        line = my_readLine(fd)
    return fileContent
