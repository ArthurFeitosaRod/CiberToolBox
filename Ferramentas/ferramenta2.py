import requests
from openai import OpenAI

# Configure sua chave de API aqui
client = OpenAI(api_key="SUA_CHAVE_AQUI")

def verificar_com_ia(dados_encontrados):
    prompt = f"""
    Analise os seguintes links e perfis encontrados para um usuário. 
    Verifique se há alta probabilidade de pertencerem à mesma pessoa com base no nome de usuário e informações públicas.
    Dados: {dados_encontrados}
    Responda com um relatório curto de veracidade.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def busca_avancada():
    username = input("Digite o username: ").replace("@", "")
    links_confirmados = []
    
    # Exemplo simplificado de busca no GitHub
    res = requests.get(f"https://api.github.com/users/{username}")
    if res.status_code == 200:
        links_confirmados.append(res.json().get("html_url"))
        bio = res.json().get("bio")
        print(f"GitHub encontrado! Bio: {bio}")

    if links_confirmados:
        print("\n--- Analisando consistência com IA ---")
        relatorio = verificar_com_ia(links_confirmados)
        print(relatorio)

# Nota: Para rodar, você precisaria da chave da API e de mais crawlers.