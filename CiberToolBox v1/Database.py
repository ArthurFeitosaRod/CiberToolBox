import sqlite3
from tkinter import messagebox
import os

Diretorio_principal = os.path.dirname(__file__)
Diretorio_Log = os.path.join(Diretorio_principal, "Bd")
class Funcs():
    def verificar_login(self, email_entry, senha_entry):
        try:
            email = email_entry.get()
            senha = senha_entry.get()
            self.conectar_db()
            # Buscamos o registro que coincida com e-mail E senha ao mesmo tempo
            query = "SELECT * FROM clientes WHERE email_cliente = ? AND senha_cliente = ?"
            self.cursor.execute(query, (email, senha))
            # Usuario recebe tupla do db (id,nome,email,senha)
            usuario = self.cursor.fetchone() # Tenta pegar uma linha
            if usuario:
                messagebox.showinfo("Login",f"Bem-vindo, {usuario[1]}!") # usuario[1] é o nome do cliente
                return True
            else:
                print("E-mail ou senha incorretos.")
                return False
            self.desconectar_db()
        except sqlite3.Error as e:
            print(f"Erro ao verificar login: {e}")
            return False
        finally:
            self.desconectar_db()
    def adicionar_clientes(self,campo_nome,campo_email,campo_senha):
        try:
            nome = campo_nome.get()
            email = campo_email.get()
            senha = campo_senha.get()
            self.conectar_db()
            # Evitar sqlInjectionsasdasd
            query = """
            INSERT INTO clientes (nome_cliente, email_cliente, senha_cliente) 
                    VALUES (?, ?, ?)"""
            # é como um format
            self.cursor.execute(query, (nome, email, senha))
            self.conn.commit()
            print(f"Cliente {nome} adicionado com sucesso!")
            return True

        except Exception as e:
            print(f"Erro ao Adicionar um cliente: {e}") # Isso vai te dizer o erro real no console
        finally:
            self.desconectar_db()
    def limpar_clientes(self,nome,email,senha):
        pass
    def conectar_db(self):
        #conectar ou cria o banco de dados
        self.conn = sqlite3.connect(os.path.join(Diretorio_Log,'LoginDataBase.db'), timeout=10)
        self.cursor = self.conn.cursor()
    def _tabela_existe(self, table_name):
        """Verifica se uma tabela existe consultando sqlite_master."""
        self.conectar_db()
        
        # Consulta a tabela mestra do SQLite
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        
        # Se fetchone() retornar algo, a tabela existe
        existe = self.cursor.fetchone() is not None
        
        self.desconectar_db()
        return existe
    def desconectar_db(self):
        print("Desconectando.....")
        self.conn.close()
    def criar_tables(self):
        
        # Se a tabela já existe, não executa o restante do código
        if self._tabela_existe('clientes'):
            return # Sai do método
            
        # O código abaixo só será executado se a tabela 'clientes' *não* existir.
        self.conectar_db(); print("Conectando ao Banco de Dados.....")
        self.cursor.execute("""
            CREATE TABLE clientes (
                cod INTEGER PRIMARY KEY, 
                nome_cliente CHAR(40) NOT NULL,
                email_cliente CHAR(100) NOT NULL,
                senha_cliente CHAR(20) NOT NULL
            );
        """)
        
        self.conn.commit(); print("Banco De Dados Criado!!")
        self.desconectar_db()