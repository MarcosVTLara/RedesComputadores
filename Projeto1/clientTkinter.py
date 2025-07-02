import tkinter as tk
from tkinter import ttk
from UDPClient import UDPClient
import threading
import time
import base64

class clientTkinter:
    def __init__(self):
        self.udp_client = UDPClient()
        self.table = {}
        self.ip = None
        self.port = None
        self.file = None
        self.dinamic_area = None

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
        # Define o estilo amarelo para Frame e Entry
        style = ttk.Style()
        style.configure("Yellow.TFrame", background="yellow")
        style.configure("Yellow.TEntry", fieldbackground="yellow")  # fieldbackground é o fundo interno do Entry

        # Limpa o container antes de atualizar
        for widget in container.winfo_children():
            widget.destroy()

        # Iterate over a copy of the dictionary's items
        for key, value in sorted(self.udp_client.buffer.items()):
            frame = ttk.Frame(container, style="Yellow.TFrame")
            frame.pack(pady=2, fill='x')

            entry = ttk.Entry(frame, style="Yellow.TEntry")
            self.table[key] = entry
            entry.insert(0, f"{key}: {value}")
            entry.pack(side='left', fill='x', expand=True, padx=(0, 5))

            botao_apagar = ttk.Button(frame, text="Apagar", command=lambda f=frame, k=key: self.remover_entry(f, k))
            botao_apagar.pack(side='right')

        if not self.udp_client.end_of_file:
            container.after(1000, lambda: self.atualizar_dados_recebidos(container))

    def interface(self):
        root = tk.Tk()
        root.title("App de Envio e Recebimento Dinâmico")
        root.geometry("500x600")

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

        self.error_label = ttk.Label(frame_principal, text="", foreground="red")
        self.error_label.pack(anchor='w', pady=(5, 0))

        # Área dinâmica de dados
        ttk.Label(frame_principal, text="Dados Recebidos:").pack(anchor='w', pady=(10, 0))
        self.dinamic_area = ttk.Frame(frame_principal)
        self.dinamic_area.pack(fill='both', expand=True)

        self.atualizar_dados_recebidos(self.dinamic_area)
        self.atualizar_erro()
        thread = threading.Thread(target=self.verify_file)
        thread.daemon = True  # Ensures the thread exits when the main program exits
        thread.start()
        root.mainloop()

    def verify_file(self):
        if not self.udp_client.end_of_file:  # Check if the condition is not met
            time.sleep(1)  # Wait for 1 second
            self.verify_file()  # Call itself again
            return

        time.sleep(1)  # Wait for 1 second

        # Logic to execute when end_of_file is True
        last_key = 0
        for key, value in sorted(self.udp_client.buffer.items()):
            if last_key == key:
                self.mudar_cor(key, "green")
            else:
                self.mudar_cor(key, "red")
                message_example = {
                    'typeOfMessage': 'resend',
                    'segment_index': key - 1,
                    'file': self.file,
                }
                self.udp_client.send_message(self.ip, int(self.port), message_example)
                self.atualizar_dados_recebidos(self.dinamic_area)
                self.verify_file()
                return

            last_key = key + 1
            time.sleep(1)

        self.udp_client.end_of_file = False
        self.save_file()
        # Save the file

    def save_file(self):
        with open(self.file, 'wb') as f:
            for key in sorted(self.udp_client.buffer.keys()):
                decoded_segment = base64.b64decode(self.udp_client.buffer[key])
                f.write(decoded_segment)
        print(f"File {self.file} saved successfully.")

    def mudar_cor(self, key, cor):
        entry = self.table.get(key)
        if entry:
            # Cria um estilo novo para cada cor
            style = ttk.Style()
            style.theme_use('clam')

            if cor == "red":
                style_name = "Red.TEntry"
                style.configure(style_name, fieldbackground="red")
            elif cor == "green":
                style_name = "Green.TEntry"
                style.configure(style_name, fieldbackground="green")
            else:
                return  # Cor inválida, não faz nada

            # Atualiza o estilo do Entry
            entry.configure(style=style_name)

    def atualizar_erro(self):
        if self.udp_client.error:
            self.error_label.config(text=self.udp_client.error_content)
        else:
            self.error_label.config(text="")
        self.error_label.after(500, self.atualizar_erro)  # Atualiza a cada 500ms


if __name__ == "__main__":
    var = clientTkinter()
    clientTkinter.interface(var)
