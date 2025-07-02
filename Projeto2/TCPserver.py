import os
import hashlib
import threading
from socket import *

class TCPServer:
    def __init__(self):
        self.server_port = 5000
        self.server_host = '0.0.0.0'
        self.base_path = './arquivos'

    def calcular_hash(self, file_path):
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()

    def lidar_com_cliente(self, conn, addr):
        print(f"\nConexão de {addr}")
        try:
            requisicao = conn.recv(1024).decode()

            if requisicao.startswith("ARQUIVO|"):
                nome_arquivo = requisicao.split("|")[1].strip()
                caminho_arquivo = os.path.join(self.base_path, nome_arquivo)

                if not os.path.exists(caminho_arquivo):
                    conn.sendall("STATUS|ERRO_ARQUIVO_NAO_ENCONTRADO\n".encode())
                    return

                tamanho = os.path.getsize(caminho_arquivo)
                hash_arquivo = self.calcular_hash(caminho_arquivo)

                conn.sendall(f"STATUS|OK\n".encode())
                conn.sendall(f"NOME|{nome_arquivo}\n".encode())
                conn.sendall(f"TAMANHO|{tamanho}\n".encode())
                conn.sendall(f"HASH|{hash_arquivo}\n".encode())

                with open(caminho_arquivo, 'rb') as f:
                    while chunk := f.read(4096):
                        conn.sendall(chunk)

                print(f"Arquivo '{nome_arquivo}' enviado com sucesso para {addr}.")

            elif requisicao.startswith("CHAT|"):
                mensagem = requisicao.split("|", 1)[1].strip()
                print(f"Mensagem de {addr}: {mensagem}")
                conn.sendall(f"Feedback da mensagem: {mensagem}".encode())

            elif requisicao.strip() == "SAIR":
                print(f"Cliente {addr} solicitou encerramento.")
        except Exception as e:
            print(f"Erro com cliente {addr}: {e}")
        finally:
            conn.close()

    def runServer(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((self.server_host, self.server_port))
        server_socket.listen(5)

        print(f"Servidor escutando em {self.server_host}:{self.server_port}")

        try:
            while True:
                conn, addr = server_socket.accept()
                thread = threading.Thread(target=self.lidar_com_cliente, args=(conn, addr))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado manualmente.")
        finally:
            server_socket.close()

if __name__ == "__main__":
    server = TCPServer()
    server.runServer()
