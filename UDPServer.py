from socket import *
from threading import Thread
from ProtocolExtract import Protcol


class UDPServer:
    def __init__(self):
        self.protocol = Protcol()
        self.serverPort = 12000
        self.running = True
    
    def handle_client(self, message, clientAddress, serverSocket):
        """Função para processar cada mensagem em uma thread separada."""
        returnMessage = self.protocol.read_message(message.decode())
        if( returnMessage == None):
            self.running = False
            serverSocket.close()
            return


        for segment in returnMessage:
            serverSocket.sendto(segment.encode(), clientAddress)
            Thread.sleep(0.1)  # Simula um atraso entre o envio dos segmentos
    


    def runServer(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', self.serverPort))


        print('The server is ready to receive')
        try:
            while self.running:
                message, clientAddress = serverSocket.recvfrom(2048)
                # Cria uma nova thread para processar a mensagem recebida
                clientThread = Thread(target=self.handle_client, args=(message, clientAddress, serverSocket))
                clientThread.start()
        except OSError as e:
            print('closeing Server')

        serverSocket.close()
        print("\nServer shutting down...")


if __name__ == "__main__":
    udp_server = UDPServer()
    udp_server.runServer()
           

            
