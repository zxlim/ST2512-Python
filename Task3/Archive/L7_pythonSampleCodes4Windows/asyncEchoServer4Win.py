#!/usr/bin/env python
# Author: Karl Kwan Apr 2016
# This verson works in MS windows, the select.select only accept
# socket element. Thus, we cannot include sys.stdin (non-socket)
# in the input event watch list.
# Instead,
# this program shows statistic when any client is making connection
# to it via port 8887
# this program will be terminated when any client is making connection to it
# via port 8888
# source file: asyncEchoServer4Win.py
# using select module to apply non-blocking socket communication, to handle multi-clients
# Single thread approach
""" 
An echo server that uses select to handle multiple clients at a time. 
Entering any line of input at the terminal will exit the server. 
~ original source - http://ilab.cs.byu.edu/python/select/echoserver.html
""" 
import select 
import socket 
import sys
def safeRecv(con,size):
        try:
                buf=con.recv(size)
        except:
                buf= ""
        return buf
def serverPrompt():
        print """
        Connect to port 8089 for echo service
        Connect to port 8887 to show statistic
        Connect to port 8888 to terminate this server
       
        """

host = '0.0.0.0' # listen on any interface
port = 8089
showstatport = 8887
shutdownport = 8888
backlog = 5 
size = 1024 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen(backlog)
statserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
statserver.bind((host,showstatport)) 
statserver.listen(backlog)
shutdownserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
shutdownserver.bind((host,shutdownport)) 
shutdownserver.listen(backlog)
 
input = [server,statserver,shutdownserver]
# define a input list, and set the initial input sources
running = 1 
serverPrompt()
while running: 
        # using select.select to obtain the latest ready lists
        inputready,outputready,exceptready = select.select(input,[],[]) 
        for s in inputready: 
                if s == server: 
                        # handle the server socket 
                        client, address = server.accept()
                        print "accepted a new client from"+str(address) 
                        input.append(client)
                elif s == statserver: 
                        # handle the statserver socket 
                        anyclient, address = statserver.accept()
                        #
                        noOfclient = len(input)-3
                        # minus out server,statserver and shutdownserver
                        print "active client: "+str(noOfclient)
                        anyclient.close() # no point to keep      
                elif s == shutdownserver: 
                  # handle the shutdownserver socket 
                        anyclient, address = shutdownserver.accept()
                        running = 0
                        anyclient.close() # no point to keep   
                else:
                        # handle all the rest (client input)
                        data = safeRecv(s,size) 
                        if data: 
                                s.sendall(data) 
                        else: 
                # the client  must have closed the socket at its end.
                                print "closing a client"
                                s.close() 
                                input.remove(s)
for s in input:
        s.close()
print "Bye Bye"
