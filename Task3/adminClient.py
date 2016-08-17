#!/usr/bin/python
import socket
import sys

def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ""
if len(sys.argv) < 3:
    host = "127.0.0.1"
else:
    host = sys.argv[1]

flag = True

while flag:
    action = raw_input("Enter your action (x to stop, s to show stats, q to quit):\t")
    try:
        if action == "x":
            s = getSocket()
            port = 8888
            s.connect((host, port))
            flag = False
        elif action == "s":
            s = getSocket()
            port = 8887
            s.connect((host, port))
            print(s.recv(255))
        elif action == "q":
            flag = False
        else:
            print("Invalid input!")
            pass
    except:
        print("Connection to server failed. Try again.")
        flag = False

print("Exiting Admin Client...")
