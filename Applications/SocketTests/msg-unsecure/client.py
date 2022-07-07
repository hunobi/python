import socket

HOST = '127.0.0.1'
PORT = 3000
BUFFER = 1024

connection = socket.create_connection((HOST,PORT))

while True:
    msg = input('msg>> ')
    connection.send(msg.encode('utf8'))
    if msg == '/exit': break
    res = connection.recv(BUFFER).decode('utf8')
    print('Server:\t',res)