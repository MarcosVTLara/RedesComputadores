from socket import *
from ProtocolExtract import ExtractProtcol
from SegmentFile import SegmentFile
import os

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', serverPort))

print('The server is ready to receive')
buffer = []

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    if(message.decode() == 'close'):
        closeMessage = 'closing Server'
        serverSocket.sendto(closeMessage.encode(), clientAddress)
        serverSocket.close()

    typeOfMessage, returnMessage = ExtractProtcol(message.decode())
    match(typeOfMessage):
        case 1:
            buffer = returnMessage
            welcomeMessage = 'SendingFile'
            serverSocket.sendto(welcomeMessage.encode(), clientAddress)

            for segment in buffer:
                serverSocket.sendto(segment, clientAddress)

            serverSocket.sendto(b'EOF', clientAddress)

        case 2:
            welcomeMessage = 'SendingFile'
            serverSocket.sendto(welcomeMessage.encode(), clientAddress)
            serverSocket.sendto(buffer[returnMessage], clientAddress)
            serverSocket.sendto(b'EOF', clientAddress)

            
        case 404:
            serverSocket.sendto(returnMessage.encode(), clientAddress)
            
        case _:
            errorMessage = 'Something get wrong'
            serverSocket.sendto(errorMessage.encode(), clientAddress)
            
