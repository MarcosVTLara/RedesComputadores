from socket import *
import hashlib
import os

def checksum(data):
    return hashlib.md5(data).hexdigest()  # Usando MD5 para checksum

serverName = 'localhost'

serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
buffer = []
file_path = os.path.join(os.getcwd(), 'example.json')
try:
    with open(file_path, 'r') as file:
        message = file.read()  # Lê o conteúdo do arquivo
        clientSocket.sendto(message.encode(),(serverName, serverPort)) 
except FileNotFoundError:
    print(f"Erro: O arquivo 'example.json' não foi encontrado no diretório {os.getcwd()}.")
    clientSocket.close()
    exit()

# message, serverAddress = clientSocket.recvfrom(2048)
# print(message.decode()) 

clientSocket.close()