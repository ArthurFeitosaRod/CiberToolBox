import customtkinter as ctk
from LoginWindow import *
class MainWindows(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("hello world")
        self.geometry("500x500")
        self.title("LOGIN")
    def Desenhar(self):
        pass
if __name__ == "__main__":
    win = Janela_Login()
    win.mainloop()