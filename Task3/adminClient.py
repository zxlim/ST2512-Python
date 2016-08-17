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
    msg = raw_input("Enter your action (/help) for help: ")
    action = msg.split()[0].replace("/","")
    try:
        if action == "help":
            print """
                /stats to retrieve current users information
                /echo [MESSAGE] to broadcast a message
                /whisper [NICKNAME] [MESSAGE] to send a private message to a user
                /kick [NICKNAME] to kick and disconnects a user
                /shutdown to shutdown the server
                /quit to disconnect from the server
                """
        elif action == "stats" or action == "s":
            s = getSocket()
            port = 8887
            s.connect((host, port))
            print(s.recv(255))
        elif action == "echo" or action == "e":
            s = getSocket()
            port = 8089
        elif action == "whisper" or action == "w":
            s = getSocket()
            port = 8885
        elif action == "kick" or action == "k":
            s = getSocket()
            port = 8886
        elif action == "shutdown":
            s = getSocket()
            port = 8888
            s.connect((host, port))
            flag = False
        elif action == "quit" or action == "q":
            flag = False
        else:
            print("Invalid input!\tEnter /help for help!\n")
            pass
    except:
        print("Connection to server failed. Try again.")
        flag = False

print("Exiting Admin Client...")
