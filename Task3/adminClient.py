#!/usr/bin/env python
#source file: simClient.py
import socket
import os
import threading
import re
import sys

checkCommand = re.compile(r"^/")
clear = lambda: os.system("cls")

def getnewsocket():
	return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def monitor(con):
    con.setblocking(True)
    con.settimeout(3.0)
    while True:
        try:
                buf = con.recv(255)
                if len(buf) > 0:
                        print buf
                else:
                        break
        except Exception as inst:
                if str(inst) != "timed out":
                    break
    print "Connection is closed"
    sys.exit()

def kickUser(user):
    #clientsocket.sendall("[" + userName + "] was kicked." + "\n")

def whisperToUser(user, msg):
        BUFFER = con.recv(255)
        BUFFER = msg

        client.send(BUFFER)

# start of main program
clear()

if len(sys.argv)<3:
    print "\n\n\n\n\nUsage:",sys.argv[0]," Server_IP User_Name"
    # program still proceeds, using the following two default settings.
    host = 'localhost'
    nickName = 'Chat-Admin'
else:
    host = sys.argv[1]
    nickName= sys.argv[2]

print "\nConnecting...\n"

try:
    clientsocket = getnewsocket()
    clientsocket.connect((host, 8089))
except:
    print "\nConnection Failed. Please try again later.\n"
    sys.exit()

t = threading.Thread(target=monitor, args=(clientsocket,))
t.start()

print "Connection successful!"
print "There are" + "<HOW>"+ "clients connected."
print "Enter (q)uit or e(x)it to disconnect."
print "Type [/help] for commands.\n"

while True:
    try:
        msg = raw_input("")
        if (msg.lower() == 'q' or \
            msg.lower() == 'quit' or \
            msg.lower() == 'x' or \
            msg.lower() == 'exit'):
        	break
        elif (checkCommand.search(msg)): # check if the message is a command
            command = msg.split()[0].replace("/","")
            if command == "help":
                print "\n/list - Lists all connected clients in the format [IP_ADDR], [NICKNAME]"
                print "/kick [NICKNAME] - Kicks and disconnects the user specified"
                print '/whisper [NICKNAME] "MESSAGE" - Sends a private message to the user specified'
                print "/shutdown - Shuts down the chat server\n"
            elif command == "list":
                print "\n\n127.0.0.1, ChatAdmin\n"
            elif command == "kick":
                userName = str(msg.split()[1])
                # validation for user input if they did not enter [NICKNAME] still needed
            elif command == "whisper":
                userName = str(msg.split()[1])
                message = str(msg.split()[2])
                whisperToUser(userName, message)
            elif command == "shutdown":
                print "Shutting down.."
            else:
                print "\nDid you enter wrongly? "

        else:
            clientsocket.sendall("\033[93m[" + nickName + "]:\033[0m" + msg + "\n")
    except:
        print "Oops! There was an error! Please try again later!"
        break
    #msg = raw_input
	#clientsocket.send(msg)
clientsocket.close()

print ""
print "Disconnected successfully!\n"
