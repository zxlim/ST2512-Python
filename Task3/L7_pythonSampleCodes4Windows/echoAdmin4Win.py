#!/usr/bin/env python
# Soure file: echoAdmin4Win.py
# Author: Karl Kwan July 2016
# By connecting to the echoserver at port 8887 and port 8888
# to send in show statistics and shutdown command
import socket
def getnewsocket():
	return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def adminConnect(portNo):
        clientsocket = getnewsocket()
        clientsocket.connect(('localhost', portNo))
        clientsocket.close()
while True:
        command = raw_input("['s'how statistics e'x'it to shutdown]=>")
        if command == 's':
                adminConnect(8887)
        elif command == 'x':
                adminConnect(8888)
                break
print "Bye Bye"
