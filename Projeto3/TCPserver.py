import os
import threading
from socket import *

class HTTPServer:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 8080
        self.base_path = './arquivos'

    def run_server(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Servidor HTTP rodando em http://{self.host}:{self.port}")

        try:
            while True:
                conn, addr = server_socket.accept()
                thread = threading.Thread(target=self.tratar_cliente, args=(conn, addr))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado manualmente.")
        finally:
            server_socket.close()

    def tratar_cliente(self, conn, addr):
        try:
            request = conn.recv(1024).decode(errors='ignore')
            print(f"\nRequisição de {addr}:")
            print(request.strip())

            linhas = request.splitlines()
            if not linhas:
                conn.close()
                return

            metodo, caminho, _ = linhas[0].split()
            caminho_arquivo = os.path.join(self.base_path, caminho.lstrip('/'))

            if metodo != 'GET':
                self.enviar_resposta(conn, 405, "Método não permitido", "text/html")
            elif not os.path.exists(caminho_arquivo):
                self.enviar_resposta(conn, 404, "Arquivo não encontrado", "text/html")
            else:
                with open(caminho_arquivo, 'rb') as f:
                    conteudo = f.read()
                tipo = self.detectar_tipo(caminho_arquivo)
                self.enviar_resposta(conn, 200, conteudo, tipo, is_bytes=True)

        except Exception as e:
            print(f"Erro ao processar cliente {addr}: {e}")
        finally:
            conn.close()

    def enviar_resposta(self, conn, status_code, conteudo, content_type, is_bytes=False):
        mensagens_status = {
            200: "OK",
            404: "Not Found",
            405: "Method Not Allowed"
        }
        status_msg = mensagens_status.get(status_code, "Erro")
        cabecalho = (
            f"HTTP/1.1 {status_code} {status_msg}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(conteudo)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        ).encode()

        conn.sendall(cabecalho)
        if is_bytes:
            conn.sendall(conteudo)
        else:
            conn.sendall(conteudo.encode())

    def detectar_tipo(self, caminho):
        if caminho.endswith(".html"):
            return "text/html"
        elif caminho.endswith(".jpg") or caminho.endswith(".jpeg"):
            return "image/jpeg"
        else:
            return "application/octet-stream"

if __name__ == "__main__":
    servidor = HTTPServer()
    servidor.run_server()
