import customtkinter as ctk
from LoginWindow import *

class Inicializadora:
    def __init__(self, janela_para_fechar):
        #fechamento da janela de login de vez por todas
        janela_para_fechar.destroy()
        #testando se há comunicação
        print("hello world")
        #principal
        self.app = MainWindows()
        self.app.mainloop()
class MainWindows(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Principal")
        self.geometry("400x300")

if __name__ == "__main__":
    win = Janela_Login()
    win.mainloop()