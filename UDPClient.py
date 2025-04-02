from socket import *
import hashlib

def checksum(data):
    return hashlib.md5(data).hexdigest()  # Usando MD5 para checksum

serverName = 'localhost'

serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
buffer = []

message = input('Input lowercase sentence:') 
clientSocket.sendto(message.encode(),(serverName, serverPort)) 
modifiedMessage, serverAddress = clientSocket.recvfrom(2048) 

if(modifiedMessage.decode() == 'SendingFile'):
    while True:
        packet, _ = clientSocket.recvfrom(2048)

        if packet == b'EOF':
            print("File received successfully.")
            break

        # Separando o checksum, número do pedaço e o pedaço de dados
        packet_checksum, packet_number, chunk = packet.split(b'|', 2)

        # Verificando o checksum
        if checksum(chunk) == packet_checksum.decode():
            buffer.append(chunk)
        else:
            resendMessage = 'RESEND' + packet_number
            clientSocket.sendto(resendMessage.encode(),(serverName, serverPort)) 
            print(f"Checksum mismatch for chunk {packet_number.decode()}. Retrying...")
            # Em um caso real, você pode querer pedir o pedaço novamente.

print (buffer)

clientSocket.close()