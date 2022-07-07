import socket


def create_file(filename):
    with open(filename, 'wb') as file:
        file.close()
        


HOST = ''
PORT = 3000
BUFFER = 1024

server = socket.create_server((HOST, PORT))
print('[LOG]\tUruchomiono serwer')

server.listen(1)
print('[LOG]\tOczekiwanie na połączenie...')
client, address = server.accept()

with client:
    print('[LOG]\tNawiązano połączenie z ', address)
    filename = client.recv(BUFFER).decode('utf8')
    create_file(filename)
    print('[LOG]\tPobrano nazwę pliku')
    client.send("OK".encode())
    print('[LOG]\tWysłano potwierdzenie')
    print('[LOG]\tOczekiwanie na plik...')
    with open(filename, 'ab') as file:
        print('[LOG]\tRozpoczęto pobieranie...')
        while True:
            data = client.recv(BUFFER)
            if not data: break
            file.write(data)
            client.send("OK".encode())
        file.close()

    print('[LOG]\tZakończono pobieranie pliku')
    client.send("OK".encode())
    print('[LOG]\tWysłano potwierdzenie')
