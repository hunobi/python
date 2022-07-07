import socket
import rsa

HOST = '127.0.0.1'
PORT = 3000
BUFFER = 1024
print("Generowanie kluczy")
PRIVATE, PUBLIC = rsa.get_pair_key()

server = socket.create_server((HOST, PORT))
print("Czekam na połączenie...")
server.listen(1)
client, address = server.accept()
print('Połączono z ',address[0],':',address[1])

client.send(PUBLIC)
client_public_key = client.recv(BUFFER)

with client:
    while True:
        msg = rsa.decrypt(PRIVATE, client.recv(BUFFER))
        if msg.decode('utf8') == '/exit': break
        client.send(rsa.encrypt(client_public_key, msg))
    client.close()