from socket import *
import hashlib
import json



class UDPClient:
    def __init__(self):
        self.buffer = []

    def checksum(data):
        return hashlib.md5(data).hexdigest()  # Usando MD5 para checksum

def send_message(ip, port, message_dict, expected_response):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(5)  # Optional: Set a timeout for receiving responses
    message = json.dumps(message_dict)
    clientSocket.sendto(message.encode(), (ip, port))
    
    while True:
        try:
            message_received, serverAddress = clientSocket.recvfrom(2048)
            decoded_message = message_received.decode()
            received_dict = eval(decoded_message)
            print(f"received_dict: {received_dict}")
            
            if decoded_message == expected_response:
                print("Desired response received.")
                break
        except timeout:
            print("Timeout reached. No response received.")
            break

if __name__ == "__main__":
    udp_client = UDPClient()
    ip = 'localhost'  # Replace with the server's IP address
    port = 12000  # Replace with the server's port number
    message = "arquivos.txt"  # Replace with the message you want to send
    message_example = {
        'typeOfMessage': 'extract',
        'file': message,
    }
    send_message(ip, port, message_example, "ACK")  # Replace "ACK" with the expected response from the server


