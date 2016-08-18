## ST2512 Programming in Security: Python Task 3 - Chat Server
## Gerald Peh Wei Xiang (P1445972), DISM/FT/2A/01
## Lim Zhao Xiang (P1529559), DISM/FT/2A/01
#!/usr/bin/python
import socket
from sys import argv
from time import sleep

def receive(s, size):
    try:
        buf = "\n" + s.recv(size)
    except:
        buf = ""
    return buf

def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

size = 255
host = ""

broadcastPort = 8884
statsPort = 8887
shutdownPort = 8888
whisperPort = 8885
kickUserPort = 8886

if len(argv) < 2:
    host = "127.0.0.1"
    print("Usage: python adminClient.py server_address")
else:
    host = argv[1]
flag = True
print("\nServer Host: " + host)

while flag:
    msg = raw_input("\nEnter your action (help) for help: ")
    action = msg.split()[0]
    try:
        s = getSocket()
        if action == "help":
            print """
stats to retrieve connected clients information
broadcast [MESSAGE] to broadcast a message
whisper [CLIENT ID] [MESSAGE] to send a private message to a user
kick [CLIENT ID] to kick and disconnects a client
shutdownNOW to shutdown the server
quit to close admin client
                """
        elif action == "stats" or action == "s":
            s.connect((host, statsPort))
            print(receive(s, size))
            s.close()
        elif action == "broadcast":
            msgFlag = True
            line = msg.replace("broadcast","")
            adminMsg = line.strip()
            if len(adminMsg) <= 0:
                print("Broadcast message is empty. Please type something.")
                msgFlag = False
            if msgFlag:
                s.connect((host, broadcastPort))
                s.sendall(adminMsg)
                s.close()
        elif action == "whisper":
            msgFlag = True
            line = msg.replace("whisper","")
            adminMsg = line.strip()
            if len(adminMsg) <= 0:
                print("Whisper input is empty. Please enter a client ID.")
                msgFlag = False
            if msgFlag:
                s.connect((host, whisperPort))
                s.sendall(adminMsg)
                print(receive(s, size))
                s.close()
        elif action == "kick":
            msgFlag = True
            line = msg.replace("kick","")
            adminMsg = line.strip()
            if len(adminMsg) <= 0:
                print("Kick input is empty. Please enter a client ID")
                msgFlag = False
            if msgFlag:
                clientID = msg.replace("kick ","")
                s.connect((host, kickUserPort))
                s.sendall(clientID)
                print(receive(s, size))
                s.close()
        elif action == "shutdownNOW":
            s.connect((host, shutdownPort))
            s.close()
            print("Server shutdown initiated.")
            flag = False
        elif action == "quit" or action == "q":
            flag = False
        else:
            print("Invalid input! Please try again.")
            pass
    except Exception as ex:
        print("Connection to server failed. Try again.")
        print(str(ex))
        sleep(1)
print("Exiting Admin Client...")
sleep(1)
