## ST2512 Programming in Security: Python Task 3 - Chat Server
## Lim Zhao Xiang (P1529559), DISM/FT/2A/01
## Gerald Peh Wei Xiang (P1445972), DISM/FT/2A/01
#!/usr/bin/python
from datetime import datetime
from select import select
import socket
from time import sleep

## Returns the current date and time
def currentDateTime():
    return datetime.now()

## Safely receives data from socket connection by catching any exceptions
def receive(client, size):
    try:
        buf = client.recv(size)
    except:
        buf = ""
    return buf

## Displays a prompt when the server starts
def prompt():
    print("Server started at:\t" + str(startTime)[:19])
    print """
Connect to port 8887 for /stats
Connect to port 8089 for /broadcast
Connect to port 8885 for /whisper
Connect to port 8886 for /kick
Connect to port 8888 for /shutdown

Server Log:
        """

## Returns the length of the clientList, which is the total number of
## clients connected
def getClientCount():
    return str(len(clientList))

## Returns a string containing the IP address, port and a unique ID
## of all connected clients
def getClientStats():
    clientID = 1
    clientStats = ""
    for c in clientList:
        temp = clientStatsDict[c] + (clientID,)
        clientStats = clientStats + str(temp[0]) + ":" + str(temp[1])\
                      + "\t|\t" + str(temp[2]) + "\n"
        clientID = clientID + 1
    return clientStats

## Assigns a unique ID based on the number of connected clients and the order
## they connected to the server
def setClientID():
    clientDict.clear()
    clientID = 1
    for c in clientList:
        clientDict[clientID] = c
        clientID = clientID + 1

## Returns a socket
def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

size = 255
backlog = 9
host = "0.0.0.0"

echoPort = 8089
statsPort = 8887
shutdownPort = 8888
broadcastPort = 8884
whisperPort = 8885
kickUserPort = 8886

echo = getSocket()
stats = getSocket()
shutdown = getSocket()
broadcast = getSocket()
whisper = getSocket()
kickUser = getSocket()

echo.bind((host, echoPort))
echo.listen(backlog)

stats.bind((host, statsPort))
stats.listen(backlog)

shutdown.bind((host, shutdownPort))
shutdown.listen(backlog)

broadcast.bind((host, broadcastPort))
broadcast.listen(backlog)

whisper.bind((host, whisperPort))
whisper.listen(backlog)

kickUser.bind((host, kickUserPort))
kickUser.listen(backlog)

inputList = [echo, stats, shutdown, broadcast, whisper, kickUser]
clientList = []
clientStatsDict = {}
clientDict = {}
flag = True
startTime = currentDateTime()
prompt()

while flag:
    inputready, outputread, exceptready = select(inputList, [], [])
    for s in inputready:
        if s == echo:
            c, addr = echo.accept()
            for client in clientList:
                client.sendall("Someone has joined the chat.\n")
            inputList.append(c)
            clientList.append(c)
            clientStatsDict[c] = (addr[0], addr[1])
            print(addr[0] + ":" + str(addr[1]) + " connected to the server.\n"\
                  + "Clients connected: " + getClientCount())
        elif s == stats:
            a, addr = stats.accept()
            upTime = currentDateTime() - startTime
            adminStats = "Server has been up for " + str(upTime)[:10]\
                         + "\nClients connected: " + getClientCount()\
                         + "\nIP Address\t|\tClient ID\n" + getClientStats()
            a.sendall(adminStats)
            a.close()
        elif s == shutdown:
            a, addr = shutdown.accept()
            print("Server is shutting down...")
            flag = False
            a.close()
            for client in clientList:
                client.sendall("Chat server is shutting down...\n")
            sleep(2)
        elif s == broadcast:
            a, addr = broadcast.accept()
            buf = receive(a, size)
            print("An admin has broadcasted a message.")
            for client in clientList:
                client.sendall("Server Broadcast: " + buf + "\n")
            a.close()
        elif s == whisper:
            a, addr = whisper.accept()
            buf = receive(a, size)
            clientID = buf[0]
            msg = buf[2:]
            setClientID()
            try:
                client = clientDict[int(clientID)]
                client.sendall("Private Message from Admin: " + msg + "\n")
                a.sendall("Private message sent successfully.\n")
                print("An admin has whispered to Client ID " + clientID)
            except Exception as ex:
                a.sendall("Server encountered an error:\n" + str(ex) + "\n")
                pass
            a.close()
        elif s == kickUser:
            a, addr = kickUser.accept()
            buf = receive(a, size)
            setClientID()
            try:
                client = clientDict[int(buf)]
                client.close()
                inputList.remove(client)
                clientList.remove(client)
                del clientStatsDict[client]
                print("Client ID " + str(buf) + " kicked from server.")
                a.sendall("Client ID " + str(buf) + " kicked from server.\n")
                for c in clientList:
                    c.sendall("Someone has been kicked from the chat.\n")
                    c.sendall(getClientCount() + " person(s) left.\n")
            except Exception as ex:
                a.sendall("Server encountered an error:\n" + str(ex) + "\n")
                pass
            a.close()
        else:
            buf = receive(s, size)
            if buf:
                for client in clientList:
                    client.sendall(buf)
            else:
                try:
                    c = clientStatsDict[s]
                    s.close()
                    inputList.remove(s)
                    clientList.remove(s)
                    del clientStatsDict[s]
                    for client in clientList:
                        client.sendall("Someone left the chat.\n")
                        client.sendall(getClientCount() + " person(s) left.\n")
                    print(str(c[0]) + ":" + str(c[1])\
                          +" disconnected from the server.")
                    print("Clients connected: " + getClientCount())
                except Exception as ex:
                    print("Server encountered an error:\n" + str(ex))
                    pass
for client in clientList:
    client.close()
print("Server connection closed.")
