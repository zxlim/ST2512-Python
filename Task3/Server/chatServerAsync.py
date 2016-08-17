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
        Connect to port 8089 for echo service
        Connect to port 8887 to show statistic
        Connect to port 8888 to terminate this server
        """

def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

size = 1024
backlog = 10
host = "0.0.0.0"
port = 8089
statsPort = 8887
shutdownPort = 8888
echo = getSocket()
stats = getSocket()
shutdown = getSocket()
echo.bind((host, port))
echo.listen(backlog)
stats.bind((host, port))
stats.listen(backlog)
shutdown.bind((host, port))
shutdown.listen(backlog)
inputList = [echo, stats, shutdown]
clientList = []
prompt()
flag = True
while flag:
    inputready, outputread, exceptready = select.select(inputList, [], [])
    for s in inputready:
        if s == echo:
            c, addr = server.accept()
            print("Remote connection from " + addr[0] + " accepted.")
            inputList.append(c)
            clientList.append(c)
        elif s == stats:
            statsClient, addr = server.accept()
            statsClient.sendall("Clients connected: " + str(len(clientList)))
            statsClient.close()
        elif s == shutdown:
            shutdownClient, addr = server.accept()
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
