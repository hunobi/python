import sys
import socket


def get_name_file_from_path(path):
    t = path.split('\\')
    return t[len(t)-1]


def count_chunks_from_file(path, buffer):
    n = 0
    with open(path, 'rb') as file:
        while(chunk := file.read(buffer)):
            n = n + 1
    return n

def send_file(conn, filename, buffer, chunks):
    n = 0
    tmp = None
    with open(filename, 'rb') as file:
        while(chunk := file.read(buffer)):
            if n == chunks-1:
                tmp = chunk
                break
            conn.send(chunk)
            conn.recv(buffer)
            n = n + 1
            print("Client:\t [" + str(n)+"/" + str(chunks)+"]\r", end='')
        file.close()
        conn.send(tmp)
        n = n + 1
        print("Client:\t [" + str(n)+"/" + str(chunks)+"]\r")


FILE_PATH = sys.argv[1]
FILE_NAME = get_name_file_from_path(FILE_PATH)
HOST = '192.168.178.21'
PORT = 3000
BUFFER = 1024
CHUNKS = count_chunks_from_file(FILE_PATH, BUFFER)

connection = socket.create_connection((HOST,PORT))
print("Client:\t", "Wysyłam nazwę pliku")
connection.send(FILE_NAME.encode('utf8'))
# czekam na odpowiedz
res= connection.recv(BUFFER).decode('utf8')
print("Server:\t", res)
print("Client:\t", "Segmentów do wysłania: " + str(CHUNKS))
print("Client:\t", "Trwa wysyłanie...")
send_file(connection, FILE_PATH, BUFFER, CHUNKS)
print("Client:\t", "Plik został przesłany")
print("Client:\t", "Trwa oczekiwanie na potwierdzenie..")
res = connection.recv(BUFFER).decode('utf8')
print("Server:\t", res)
connection.close()
print("Client:\t", "Koniec")
