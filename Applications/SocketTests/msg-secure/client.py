import socket
import rsa

HOST = '127.0.0.1'
PORT = 3000
BUFFER = 1024

print("Generowanie kluczy")
PRIVATE, PUBLIC= rsa.get_pair_key()

connection = socket.create_connection((HOST,PORT))

server_public_key = connection.recv(BUFFER)
connection.send(PUBLIC)

while True:
    msg = input('msg>> ')
    connection.send(rsa.encrypt(server_public_key, msg.encode('utf8')))
    if msg == '/exit': break
    res = rsa.decrypt(PRIVATE, connection.recv(BUFFER)).decode('utf8')
    print('Server:\t',res)