from socket import *
import json

class UDPClient:
    def __init__(self):
        self.buffer = {}
        self.end_of_file = False
        self.error = False
        self.error_content = None

    def send_message(self, ip, port, message_dict):
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(3)  # colocar tempo entre mensagens recebidas
        message = json.dumps(message_dict)
        clientSocket.sendto(message.encode(), (ip, port))
        
        while True:
            #Armazenar resposta no buffer
            try:
                message_received, serverAddress = clientSocket.recvfrom(8192)
                decoded_message = message_received.decode()
                received_dict = eval(decoded_message)
                if 'error' in received_dict:
                    self.error = True
                    self.error_content = received_dict['error']
                    break
                self.buffer[received_dict['segment_index']] = received_dict['data']
                self.end_of_file = received_dict['is_last']
                if self.end_of_file:
                    break
            except timeout:
                print("Timeout reached. No response received.")
                break
