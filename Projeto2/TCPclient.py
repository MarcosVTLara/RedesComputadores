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

    def receber_linha(self):
        """Lê uma linha completa terminada por '\n'."""
        buffer = b''
        while b'\n' not in buffer:
            parte = self.connection.recv(1024)
            if not parte:
                break
            buffer += parte
        return buffer.decode().strip()

    def receber_arquivo(self, nome_arquivo):
        self.send_request(f"ARQUIVO|{nome_arquivo}")

        status = self.receber_linha()
        if "ERRO" in status:
            print("Arquivo não encontrado no servidor.")
            return

        # Recebe NOME
        linha_nome = self.receber_linha()
        partes_nome = linha_nome.split("|")
        if len(partes_nome) < 2:
            print("Erro no protocolo ao receber o nome do arquivo:", linha_nome)
            return
        nome = partes_nome[1].strip()

        # Recebe TAMANHO
        linha_tamanho = self.receber_linha()
        partes_tamanho = linha_tamanho.split("|")
        if len(partes_tamanho) < 2:
            print("Erro no protocolo ao receber o tamanho do arquivo:", linha_tamanho)
            return
        tamanho = int(partes_tamanho[1])

        # Recebe HASH
        linha_hash = self.receber_linha()
        partes_hash = linha_hash.split("|")
        if len(partes_hash) < 2:
            print("Erro no protocolo ao receber o hash do arquivo:", linha_hash)
            return
        hash_servidor = partes_hash[1].strip()

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
        resposta = self.receber_linha()
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
