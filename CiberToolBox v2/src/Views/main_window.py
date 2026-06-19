import customtkinter as ctk

class ClientView(ctk.CTk):
    def  __init__(self):
        super().__init__()        
        self.title("CibertoolBox/Menu")
        self.eval('tk::PlaceWindow . center')
        self.geometry("650x400")
        self.resizable(False,False)
    