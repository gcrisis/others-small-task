import socket

serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = socket.gethostname()
port = 444

serversocket.bind(('localhost',port))

serversocket.listen(3)
print ('begin listen')

while True:

    newsocket,address = serversocket.accept()

    print('get request from: %s' %str(address))

    msgback='this is the message from server'

    newsocket.send(msgback)

    newsocket.close()


