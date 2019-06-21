import socket

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

port = 444

clientsocket.connect(('localhost',port))


a = clientsocket.recv(1024)

print (a)

clientsocket.close()
