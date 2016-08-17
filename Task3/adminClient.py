#!/usr/bin/python
import socket
import sys

def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ""
if len(sys.argv) < 3:
    host = "127.0.0.1"
else:
    host = sys.ar/
    gv[1]

flag = True

while flag:
    msg = raw_input("Enter your action (/h) for help: ")
    action = msg.split()[0].replace("/","")
    try:
        if action == "help":
            print """
                /kick [NICKNAME] - Kicks and disconnects the user specified"
                /whisper [NICKNAME] "MESSAGE" - Sends a private message to the user specified
                /shutdown to shutdown the server
                /stats to retrieve current users information
                /quit to disconnect from the server
                """
        elif action == "shutdown":
            s = getSocket()
            port = 8888
            s.connect((host, port))
            flag = False
        elif action == "stats":
            s = getSocket()
            port = 8887
            s.connect((host, port))
            print(s.recv(255))
        elif action == "quit":
            flag = False
        else:
            print("Invalid input!")
            pass
    except:
        print("Connection to server failed. Try again.")
        flag = False

print("Exiting Admin Client...")
