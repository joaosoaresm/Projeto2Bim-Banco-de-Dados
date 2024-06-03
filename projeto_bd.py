import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Função para conectar ao banco de dados
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projetobd"
    )

# Função para cadastrar parceiro
def cadastrar_parceiro(usuario_nome):
    parceiro_window = tk.Tk()
    parceiro_window.title("Cadastro de Parceiro")
    parceiro_window.geometry("400x400")

    parceiro_nome_label = tk.Label(parceiro_window, text="Nome do Parceiro:")
    parceiro_nome_label.pack(pady=5)
    parceiro_nome_entry = tk.Entry(parceiro_window)
    parceiro_nome_entry.pack(pady=5)

    genero_label = tk.Label(parceiro_window, text="Gênero do Parceiro:")
    genero_label.pack(pady=5)
    generos = ['Masculino', 'Feminino', 'Outro']
    genero_combobox = ttk.Combobox(parceiro_window, values=generos, state="readonly")
    genero_combobox.pack(pady=5)

    hobbies_label = tk.Label(parceiro_window, text="Hobbies do Parceiro:")
    hobbies_label.pack(pady=5)
    hobbies = ['Esportes', 'Leitura', 'Música', 'Cozinha', 'Tecnologia']
    hobbies_combobox = ttk.Combobox(parceiro_window, values=hobbies, state="readonly")
    hobbies_combobox.pack(pady=5)

    def cadastrar():
        parceiro_nome = parceiro_nome_entry.get()
        genero = genero_combobox.get()
        hobbies = hobbies_combobox.get()

        if parceiro_nome and genero and hobbies:
            conn = conectar_db()
            cursor = conn.cursor()
            query = "INSERT INTO Parceiro (nome, genero, hobbies) VALUES (%s, %s, %s)"
            cursor.execute(query, (parceiro_nome, genero, hobbies))
            parceiro_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", f"Parceiro cadastrado com sucesso! ID do parceiro: {parceiro_id}")
            parceiro_window.destroy()
            cadastrar_usuario(usuario_nome, parceiro_id, hobbies)
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todas as informações do parceiro.")

    cadastrar_parceiro_button = tk.Button(parceiro_window, text="Cadastrar Parceiro", command=cadastrar)
    cadastrar_parceiro_button.pack(pady=10)

    parceiro_window.mainloop()

# Função para cadastrar usuário
def cadastrar_usuario(usuario_nome, parceiro_id, hobbies):
    if usuario_nome:
        conn = conectar_db()
        cursor = conn.cursor()
        print(parceiro_id, usuario_nome)
        query = "INSERT INTO Usuario (nome, Parceiro_id) VALUES (%s, %s)"
        print(query)
        cursor.execute(query, (usuario_nome, parceiro_id))
        conn.commit()
        usuario_id = cursor.lastrowid
        cursor.close()
        conn.close()
        messagebox.showinfo("Sucesso", f"Usuário cadastrado com sucesso! ID do usuário: {usuario_id}")
        buscar_presente(hobbies)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira o nome do usuário.")


# Função para buscar presente com base nos 
def buscar_presente(hobbies):
    conn = conectar_db()
    cursor = conn.cursor()

    query = """
    SELECT categoria, resultados FROM Presente
    WHERE categoria = %s
    """
    cursor.execute(query, (hobbies,))
    presentes = cursor.fetchall()

    cursor.close()
    conn.close()

    # Configura a janela para mostrar os resultados
    resultado_window = tk.Tk()
    resultado_window.title("Resultados de Presentes")
    resultado_window.geometry("400x400")

    resultado_label = tk.Label(resultado_window, text="Sugestões de Presentes:", wraplength=300)
    resultado_label.pack(pady=10)

    for presente in presentes:
        presente_label = tk.Label(resultado_window, text=f"{presente[0]} - {presente[1]}", wraplength=300)
        presente_label.pack(pady=5)

    resultado_window.mainloop()

# Função para configurar a janela de cadastro de usuário
def cadastrar_usuario_window():
    global usuario_nome_entry
    global usuario_window

    usuario_window = tk.Tk()
    usuario_window.title("Cadastro de Usuário")
    usuario_window.geometry("400x200")

    usuario_nome_label = tk.Label(usuario_window, text="Nome do Usuário:")
    usuario_nome_label.pack(pady=5)
    usuario_nome_entry = tk.Entry(usuario_window)
    usuario_nome_entry.pack(pady=5)

    cadastrar_usuario_button = tk.Button(usuario_window, text="Cadastrar Usuário", command=lambda: cadastrar_parceiro(usuario_nome_entry.get()))
    cadastrar_usuario_button.pack(pady=10)

    usuario_window.mainloop()

cadastrar_usuario_window()