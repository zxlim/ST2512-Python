#!/usr/bin/python
import select
import socket

def receive(client, size):
    try:
        buf = client.recv(size)
    except:
        buf = ""
    return buf

def prompt():
    print """
        Connect to port 8887 for /stats
        Connect to port 8089 for /broadcast
        Connect to port 8885 for /whisper
        Connect to port 8886 for /kick
        Connect to port 8888 for /shutdown
        """

def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

size = 1024
backlog = 10
host = "0.0.0.0"

statsPort = 8887
echoPort = 8089
whisperPort = 8885
kickUserPort = 8886
shutdownPort = 8888

stats = getSocket()
echo = getSocket()
#whisper = getSocket()
#kickUser = getSocket()
shutdown = getSocket()

stats.bind((host, statsPort))
stats.listen(backlog)

echo.bind((host, echoPort))
echo.listen(backlog)

#whisper.bind((host, whisperPort))
#whisper.listen(backlog)

#kickUser.bind((host, kickUserPort))
#kickUser.listen(backlog)

shutdown.bind((host, shutdownPort))
shutdown.listen(backlog)

inputList = [echo, stats, shutdown]
#inputList = [echo, stats, shutdown]
clientList = []
prompt()
flag = True
while flag:
    inputready, outputread, exceptready = select.select(inputList, [], [])
    for s in inputready:
        if s == echo:
            c, addr = echo.accept()
            print("Remote connection from " + addr[0] + " accepted.")
            inputList.append(c)
            clientList.append(c)
        elif s == stats:
            statsClient, addr = stats.accept()
            statsClient.sendall("Clients connected: " + str(len(clientList)))
            statsClient.close()
        elif s == shutdown:
            shutdownClient, addr = shutdown.accept()
            print("Shutting down server...")
            flag = False
            shutdownClient.close()
        else:
            buf = receive(s, size)
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
