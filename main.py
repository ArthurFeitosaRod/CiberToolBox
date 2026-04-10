import customtkinter as ctk
from CTkMenuBarPlus import *
from LoginWindow import *
import subprocess
import threading
import os

class Inicializadora:
    def __init__(self, janela_para_fechar):
        janela_para_fechar.destroy()
        print("hello world")
        self.app = MainWindows()
        self.app.mainloop()

class MainWindows(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.diretorio_atual = os.getcwd()
        self.title("Sistema Principal")
        self.geometry("900x600")
        
        self.configurar_grid()
        self.criar_menu_lateral()
        self.criar_area_conteudo()

    def configurar_grid(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def criar_menu_lateral(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Ferraentas
        self.btn_ferramenta = ctk.CTkButton(self.sidebar, text="Sherlock", command=self.abrir_terminal_ferramenta_a)
        self.btn_ferramenta.pack(pady=10, padx=10)
        
        self.btn_ferramentb = ctk.CTkButton(self.sidebar, text="Nmap", command=self.abrir_terminal_ferramenta_b)
        self.btn_ferramentb.pack(pady=10, padx=10)

    def criar_area_conteudo(self):
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

# terminal

    def abrir_terminal_ferramenta_a(self):
        # Lista branca de comandos para a Ferramenta A
        permitidos = ["sherlock", "ls", "cd", "cls", "clear", "dir","python3"]
        self.abrir_powershell(permitidos, "Sherlock Terminal")
    def abrir_terminal_ferramenta_b(self):
        # Lista branca de comandos para a Ferramenta A
        permitidos = ["nmap", "ls", "cd", "cls", "clear", "dir"]
        self.abrir_powershell(permitidos, "nmap")

    def abrir_powershell(self, comandos_permitidos, titulo_terminal):
        self.whitelist = comandos_permitidos
        
        for widget in self.container.winfo_children():
            widget.destroy()

        self.terminal_text = ctk.CTkTextbox(self.container, font=("Consolas", 13), fg_color="#012456", text_color="white")
        self.terminal_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.terminal_text.insert("end", f"--- {titulo_terminal} ---\n")
        self.terminal_text.insert("end", f"Permitidos: {', '.join(comandos_permitidos)}\n\nPS {os.getcwd()}> ")
        
        # O ERRO ESTAVA AQUI: A função processar_comando_ps não existia abaixo
        self.terminal_text.bind("<Return>", self.processar_comando_ps)

    def processar_comando_ps(self, event):
        """Extrai o comando da linha e envia para execução"""
        linha_inteira = self.terminal_text.get("insert linestart", "insert lineend")
        
        # Limpa o prompt visual (PS C:\...> ) para pegar só o comando
        if ">" in linha_inteira:
            comando = linha_inteira.split(">")[-1].strip()
        else:
            comando = linha_inteira.strip()

        if comando:
            # Executa em Background para não travar a interface
            threading.Thread(target=self.executar_no_sistema, args=(comando,), daemon=True).start()
        
        self.terminal_text.insert("end", "\n")
        return "break" 

    def executar_no_sistema(self, comando):
        """Lógica de permissão e execução real no PowerShell"""
        partes = comando.split()
        if not partes: return
        
        cmd_base = partes[0].lower()

        # Verificação de Permissão (Whitelist)
        if cmd_base not in self.whitelist:
            self.terminal_text.insert("end", f"\n[ACESSO NEGADO] O comando '{cmd_base}' não pertence a esta ferramenta.\nPS {os.getcwd()}> ")
            self.terminal_text.see("end")
            return

        try:
            # Lógica para CD (Mudar Pasta)
            if cmd_base in ["cd", "entrar"]:
                caminho = comando.replace(partes[0], "").strip()
                if not caminho: caminho = os.path.expanduser("~")
                os.chdir(os.path.abspath(os.path.join(os.getcwd(), caminho)))
                saida = ""
            if cmd_base in ["nmap"]:
                self.terminal_text.insert("end",f"\nEscaneando...\nPS {os.getcwd()}> ")
                self.terminal_text.see("end")
                return
            
            # Lógica para CLS (Limpar Tela)
            elif cmd_base in ["cls", "clear"]:
                self.terminal_text.delete("1.0", "end")
                self.terminal_text.insert("end", f"PS {os.getcwd()}> ")
                return

            else:
                # Executa comandos permitidos (ls, dir, sherlock...)
                resultado = subprocess.run(
                    ["powershell", "-Command", comando], 
                    capture_output=True, 
                    text=True, 
                    encoding='cp850',
                    cwd=os.getcwd()
                )
                saida = resultado.stdout if resultado.stdout else resultado.stderr

            self.terminal_text.insert("end", f"{saida}\nPS {os.getcwd()}> ")
            self.terminal_text.see("end")

        except Exception as e:
            self.terminal_text.insert("end", f"\nErro: {e}\nPS {os.getcwd()}> ")
            self.terminal_text.see("end")
#auxiliar
class ProcessadorDados:
    def __init__(self):
        pass

    def validar_permissao(self, usuario):
        print(f"Verificando acesso para {usuario}...")
        return True

    def executar_calculo_ferramenta(self, dados):
        resultado = sum(dados) 
        return resultado

    def salvar_relatorio(self, conteudo):
        with open("log.txt", "a") as f:
            f.write(conteudo + "\n")
        print("Relatório salvo com sucesso!")

if __name__ == "__main__":
    win = Janela_Login()
    win.mainloop()