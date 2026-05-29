import customtkinter as ctk

class ClientView(ctk.CTk):
    def  __init__(self):
        super().__init__()        
        self.title("CibertoolBox/Login")
        self.geometry("650x400")
        self.resizable(False,False)
    