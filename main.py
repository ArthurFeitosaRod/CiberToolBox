import customtkinter as ctk
from CTkMenuBarPlus import *
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
        self.geometry("900x600")
        # self.menu_bar = CTkMenuBar(self)
        # file_button = self.menu_bar.add_cascade("File")
        # 1. Def para criar a estrutura de colunas/frames
        self.configurar_grid()
        
        # 2. Def para criar o menu lateral
        self.criar_menu_lateral()
        
        # 3. Def para criar a área de exibição principal
        self.criar_area_conteudo()

    def configurar_grid(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def criar_menu_lateral(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Botões do menu (Aqui o Dev 1 chama as defs que o Dev 2 vai criar)
        self.btn_ferramenta1 = ctk.CTkButton(self.sidebar, text="Ferramenta A")
        self.btn_ferramenta1.pack(pady=10, padx=10)

    def criar_area_conteudo(self):
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
class ProcessadorDados:
    def __init__(self):
        pass

    # 1. Def para processar login/autenticação extra
    def validar_permissao(self, usuario):
        print(f"Verificando acesso para {usuario}...")
        return True

    # 2. Def para a lógica da ferramenta principal
    def executar_calculo_ferramenta(self, dados):
        # Aqui entra a matemática ou lógica complexa
        resultado = sum(dados) 
        return resultado

    # 3. Def para salvar logs ou arquivos
    def salvar_relatorio(self, conteudo):
        with open("log.txt", "a") as f:
            f.write(conteudo + "\n")
        print("Relatório salvo com sucesso!")
if __name__ == "__main__":
    win = Janela_Login()
    win.mainloop()