import socket
import hashlib
import questionary

class TCPClient:
    def __init__(self):
        self.connection = None

    def connect(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def send_request(self, mensagem):
        self.connection.sendall(mensagem.encode('utf-8'))

    def receber_resposta(self):
        return self.connection.recv(4096).decode()

    def receber_arquivo(self, nome_arquivo):
        self.send_request(f"ARQUIVO|{nome_arquivo}")

        status = self.connection.recv(1024).decode()
        if "ERRO" in status:
            print("Arquivo não encontrado no servidor.")
            return

        nome = self.connection.recv(1024).decode().split("|")[1].strip()
        tamanho = int(self.connection.recv(1024).decode().split("|")[1])
        hash_servidor = self.connection.recv(1024).decode().split("|")[1].strip()

        with open(f"recebido_{nome}", 'wb') as f:
            bytes_recebidos = 0
            while bytes_recebidos < tamanho:
                chunk = self.connection.recv(min(4096, tamanho - bytes_recebidos))
                if not chunk:
                    break
                f.write(chunk)
                bytes_recebidos += len(chunk)

        # Verificação de integridade
        sha256 = hashlib.sha256()
        with open(f"recebido_{nome}", 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)

        hash_cliente = sha256.hexdigest()
        if hash_cliente == hash_servidor:
            print("Arquivo recebido com sucesso e verificado!")
        else:
            print("Arquivo corrompido. Hash não bate.")

    def chat(self, msg):
        self.send_request(f"CHAT|{msg}")
        resposta = self.connection.recv(1024).decode()
        print("Servidor:", resposta.strip())

    def sair(self):
        self.send_request("SAIR")
        self.connection.close()

if __name__ == "__main__":
    client = TCPClient()
    ip = questionary.text("Insert the IP:").ask()
    port = int(questionary.text("Insert the Port:").ask())

    client.connect(ip, port)

    while True:
        acao = questionary.select(
            "Escolha a ação:",
            choices=["Sair", "Enviar Mensagem", "Receber Arquivo"]
        ).ask()

        if acao == "Sair":
            client.sair()
            break
        elif acao == "Enviar Mensagem":
            msg = questionary.text("Mensagem:").ask()
            client.chat(msg)
        elif acao == "Receber Arquivo":
            nome = questionary.text("Nome do arquivo a solicitar:").ask()
            client.receber_arquivo(nome)
