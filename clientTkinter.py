import tkinter as tk
from tkinter import ttk
import random
import string

# Função genérica para lidar com envio
def enviar_comando(ip_port, comando):
    ip = ip_port.split(':')[0]
    port = ip_port.split(':')[1]


# Função genérica para remover um widget de entrada
def remover_entry(frame):
    frame.destroy()

# Função para simular recebimento de dados e criar entradas dinâmicas
def simular_recebimento_dados(container):
    dado = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    frame = ttk.Frame(container)
    frame.pack(pady=2, fill='x')

    entry = ttk.Entry(frame)
    entry.insert(0, dado)
    entry.pack(side='left', fill='x', expand=True, padx=(0, 5))

    botao_apagar = ttk.Button(frame, text="Apagar", command=lambda: remover_entry(frame))
    botao_apagar.pack(side='right')

# Interface principal
def criar_interface():
    root = tk.Tk()
    root.title("App de Envio e Recebimento Dinâmico")
    root.geometry("500x400")

    # Frame principal
    frame_principal = ttk.Frame(root, padding=10)
    frame_principal.pack(fill='both', expand=True)

    # Entradas de IP:PORT e Comando
    ip_port_var = tk.StringVar()
    comando_var = tk.StringVar()

    ttk.Label(frame_principal, text="IP:PORT").pack(anchor='w')
    ip_port_entry = ttk.Entry(frame_principal, textvariable=ip_port_var)
    ip_port_entry.pack(fill='x')

    ttk.Label(frame_principal, text="Comando").pack(anchor='w', pady=(10, 0))
    comando_entry = ttk.Entry(frame_principal, textvariable=comando_var)
    comando_entry.pack(fill='x')

    # Botão de envio
    def ao_enviar():
        enviar_comando(ip_port_var.get(), comando_var.get())

    enviar_btn = ttk.Button(frame_principal, text="Enviar", command=ao_enviar)
    enviar_btn.pack(pady=10)

    # Área dinâmica de dados
    ttk.Label(frame_principal, text="Dados Recebidos:").pack(anchor='w', pady=(10, 0))
    area_dinamica = ttk.Frame(frame_principal)
    area_dinamica.pack(fill='both', expand=True)

    # Botão para simular recebimento de dados
    simular_btn = ttk.Button(frame_principal, text="Simular Recebimento de Dados",
                             command=lambda: simular_recebimento_dados(area_dinamica))
    simular_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
