import tkinter as tk
from tkinter import ttk
from UDPClient import UDPClient
import threading
import time

class clientTkinter:
    def __init__(self):
        self.udp_client = UDPClient()
        self.table = {}
        self.ip = None
        self.port = None
        self.file = None

    def enviar_comando(self, ip_port):
        def enviar():
            self.ip = ip_port.split(':')[0]
            port_file = ip_port.split(':')[1]
            self.port = port_file.split('/')[0]
            self.file = ip_port.split('/')[1]
            message_example = {
                'typeOfMessage': 'extract',
                'file': self.file,
            }
            self.udp_client.send_message(self.ip, int(self.port), message_example)

        # Executa a função enviar em uma nova thread
        thread = threading.Thread(target=enviar)
        thread.start()

    def remover_entry(self, frame, key):
        frame.destroy()
        # Remove the corresponding entry widget from the table
        if key in self.table:
            del self.table[key]
        # Remove the element from the buffer
        if key in self.udp_client.buffer:
            del self.udp_client.buffer[key]

    def atualizar_dados_recebidos(self, container):
        # Limpa o container antes de atualizar
        for widget in container.winfo_children():
            widget.destroy()

        for key, value in self.udp_client.buffer.items():
            frame = ttk.Frame(container)
            frame.pack(pady=2, fill='x')

            entry = ttk.Entry(frame)
            self.table[key] = entry
            entry.insert(0, f"{key}: {value}")
            entry.pack(side='left', fill='x', expand=True, padx=(0, 5))

            botao_apagar = ttk.Button(frame, text="Apagar", command=lambda f=frame, k=key: self.remover_entry(f, k))
            botao_apagar.pack(side='right')

        print('self.udp_client.end_of_file: ', self.udp_client.end_of_file)
        if self.udp_client.end_of_file:
            self.verify_file()

        container.after(500, lambda: self.atualizar_dados_recebidos(container))

    def interface(self):
        root = tk.Tk()
        root.title("App de Envio e Recebimento Dinâmico")
        root.geometry("500x400")

        # Frame principal
        frame_principal = ttk.Frame(root, padding=10)
        frame_principal.pack(fill='both', expand=True)

        # Entradas de IP:PORT e Comando
        ip_port_var = tk.StringVar()

        ttk.Label(frame_principal, text="IP:PORT/file").pack(anchor='w')
        ip_port_entry = ttk.Entry(frame_principal, textvariable=ip_port_var)
        ip_port_entry.pack(fill='x')

        enviar_btn = ttk.Button(frame_principal, text="Enviar", command=lambda: self.enviar_comando(ip_port_var.get()))
        enviar_btn.pack(pady=10)

        # Área dinâmica de dados
        ttk.Label(frame_principal, text="Dados Recebidos:").pack(anchor='w', pady=(10, 0))
        area_dinamica = ttk.Frame(frame_principal)
        area_dinamica.pack(fill='both', expand=True)

        self.atualizar_dados_recebidos(area_dinamica)
        root.mainloop()

    def verify_file(self):
        last_key = 0
        for key in self.udp_client.buffer.items():

            if (last_key == key[0]):
                self.mudar_cor(key[0], "green")
            else:
                self.mudar_cor(key[0], "red")
                message_example = {
                    'typeOfMessage': 'resend',
                    'segment_index': key[0],
                    'file': self.file,
                }
                self.udp_client.send_message(self.ip, int(self.port), message_example)
                self.verify_file()

            last_key = key[0]
            time.sleep(1)
            
        #Save the file
            
    def mudar_cor(self, key, cor):
        if key not in self.table:
            return

        entry_widget = self.table[key]
        style = ttk.Style()
        estilo = f"{str(entry_widget)}.TEntry"

        if cor == "red":
            style.configure(estilo, fieldbackground="red")
        elif cor == "green":
            style.configure(estilo, fieldbackground="green")

        entry_widget.configure(style=estilo)

if __name__ == "__main__":
    var = clientTkinter()
    clientTkinter.interface(var)
