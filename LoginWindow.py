from tkinter import *
from tkinter import messagebox
import sys
from Database import Funcs

class Janela_Login(Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("310x330")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')
        self.__db_funcs = Funcs()
        self.__db_funcs.criar_tables()
        self.config(bg="#FFFFFF")
        self.login()
    def cadastrar(self):
        Janela_Login.withdraw(self)
        win = Janela_Cadastro()
    def fechar_tudo(self):
        """Fecha todas as janelas e encerra o programa."""
        self.destroy()
        self.__db_funcs.desconectar_db()
        sys.exit(0)
    def login(self):
        """Identifica o fechamento(x)"""
        self.protocol("WM_DELETE_WINDOW", self.fechar_tudo)
        login = Label(self, text="LOGIN", font="bold 35", pady=10)
        login.place(x=5, y=0)
        email_label = Label(self, anchor=NE, text=f"Email ", font="16")
        email_label.place(x=5, y=100)
        Label(self, text='*', font="16", fg="#ff0000").place(x=55, y=100)
        email_entry = Entry(self, width="40", relief="solid")
        email_entry.place(x=5, y=130)
        senha_label = Label(self, anchor=NE, text="Senha ", font="16")
        senha_label.place(x=5, y=160)
        Label(self, text='*', font="16", fg="#ff0000").place(x=55, y=160)
        senha_entry = Entry(self, width="40", relief="solid")
        senha_entry.place(x=5, y=190)
        self.linha_divisoria()
        # Interações de login/Cadastro
        botao = Button(self, text="ENTRAR", bg="#6a6666", width="15", command=lambda: self.login_db(email_entry,senha_entry))
        botao.place(x=5, y=230)
        botao_cadastro = Button(self, text="Não tem login?", bg="#ffffff", bd=0, activeforeground="#ffffff", width="15", command=self.cadastrar)
        botao_cadastro.place(x=130, y=230)
    def linha_divisoria(self):
        frame_cima = Frame(self, width=350, height=5, bg="#50504d", relief="flat")
        frame_cima.place(x=5, y=60)
    def login_db(self, email_entry, senha_entry):
        # Chama a função que criamos acima
        sucesso = self.__db_funcs.verificar_login(email_entry, senha_entry)
        email_entry.delete(0, END)
        senha_entry.delete(0, END)
        if sucesso:
            # Lógica para abrir a próxima tela ou mostrar mensagem de sucesso
            messagebox.showinfo("Login", "Entrada autorizada!")
            self.fechar_tudo()
        else:
            # Lógica para erro
            messagebox.showerror("Erro", "Usuário ou senha inválidos")
class Janela_Cadastro(Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro")
        self.geometry("310x330")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')
        self.__db_funcs = Funcs()
        self.__db_funcs.criar_tables()
        self.cadastro()
    def fechar_tudo(self):
        """Fecha todas as janelas e encerra o programa."""
        self.destroy()
        sys.exit(0)
    def cadastro_db(self,campo_nome,campo_email,campo_senha):
        # adicionar os campos no database
        self.__db_funcs.adicionar_clientes(campo_nome,campo_email,campo_senha)
        
        # forma rapida que achei para deletar apos o clique
        campo_nome.delete(0, END)
        campo_email.delete(0, END)
        campo_senha.delete(0, END)

    def cadastro(self):
        """Identifica o fechamento(x)"""
        self.protocol("WM_DELETE_WINDOW", self.fechar_tudo)
        cadastro = Label(self, text="CADASTRO", font="bold 35")
        cadastro.place(x=5, y=5)
        # Dividindo a tela
        frame_cima = Frame(self, width=350, height=5, bg="#4e0000", relief="flat")
        frame_cima.place(x=5, y=65)
        #nome
        nome = Label(self, anchor=NE, text="Nome ", font="16")
        nome.place(x=5, y=100)
        Label(self, text='*', font="16", fg="#ff0000").place(x=55, y=100)
        campo_nome = Entry(self, width="40", relief="solid")
        campo_nome.place(x=5, y=130)
        # Email
        email = Label(self, anchor=NE, text="Email ", font="16")
        email.place(x=5, y=155)
        Label(self, text='*', font="16", fg="#ff0000").place(x=55, y=155)
        campo_email = Entry(self, width="40", relief="solid")
        campo_email.place(x=5, y=185)
        # Senha
        Senha2 = Label(self, anchor=NE, text="Senha ", font="16")
        Senha2.place(x=5, y=210)
        Label(self, text='*', font="16", fg="#ff0000").place(x=55, y=210)
        campo_senha = Entry(self, width="40", relief="solid")
        campo_senha.place(x=5, y=230)
        # Botão de cadastro
        botao = Button(self, text="ENTRAR", bg="#5e5e5e", width="15", command=lambda: self.cadastro_db(campo_nome,campo_email,campo_senha))
        # lambda é para passar argumentos dentro da função
        botao.place(x=5, y=250)
        # Botão para ir para a tela de login
        botao_Login = Button(self, text="já tem login?", bg="#ffffff", bd=0, activeforeground="#ffffff", width="15", command=self.Logar)
        botao_Login.place(x=170, y=250)
    def Logar(self):
        Janela_Cadastro.destroy(self)
        Janela_Login().deiconify()
if __name__ == "__main__":
    win = Janela_Login()
    win.mainloop()