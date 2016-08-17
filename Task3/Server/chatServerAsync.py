#!/usr/bin/python
import select
import socket
import sys
import time

def prompt():
    print("\nType x to close server\nType s to show statistics")

def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

size = 255
host = "0.0.0.0"
port = 8089
server = getSocket()
server.bind((host, port))
server.listen(10)
inputList = [server, sys.stdin]
clientList = []
prompt()
flag = True
while flag:
    inputready, outputread, exceptready = select.select(inputList, [], [])
    for s in inputready:
        if s == server:
            c, addr = server.accept()
            print("Remote connection from " + addr[0] + " accepted.")
            inputList.append(c)
            clientList.append(c)
        elif s == sys.stdin:
            cmd = sys.stdin.readline().strip()
            if cmd == "x":
                flag = False
            elif cmd == "s":
                print("Clients connected: " + str(len(clientList)))
                prompt()
            else:
                prompt()
        else:
            buf = s.recv(size)
            if buf:
                #print(buf) # Debug code
                for client in clientList:
                    client.sendall(buf)
            else:
                s.close()
                inputList.remove(s)
                clientList.remove(s)
                #print("Connection from " + addr + " closed.")
                print("Clients connected: " + str(len(clientList)))
for client in clientList:
    client.close()
print("Server connection closed.")
