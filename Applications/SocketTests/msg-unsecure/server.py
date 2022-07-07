import socket

HOST = '127.0.0.1'
PORT = 3000
BUFFER = 1024

# utworzenie instancji serwera
server = socket.create_server((HOST, PORT))
# nasłuchiwanie na klienta
server.listen(1)
# zaakceptowanie przychodzącego połączenia
client, address = server.accept()
print('Połączono z ',address[0],':',address[1])
with client:
    # pętla komunikacji
    while True:
        # odbieramy wiadomość od klienta
        msg = client.recv(BUFFER)
        # jeżeli wysłana wiadomość to /exit - wyjdź z pętli
        if msg.decode('utf8') == '/exit': break
        print(msg.decode('utf8'))
        # odeślij wiadomość do klienta
        client.send(msg)
    # zakończ połączenie
    client.close()