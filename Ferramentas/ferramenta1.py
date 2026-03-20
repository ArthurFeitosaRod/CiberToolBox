import asyncio
import aiohttp
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import os

init(autoreset=True)

class CyberShieldOSINT:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.targets = {
            "GitHub": "https://github.com/{}",
            "Twitter": "https://twitter.com/{}",
            "Instagram": "https://www.instagram.com/{}/",
            "Pinterest": "https://www.pinterest.com/{}/",
            "YouTube": "https://www.youtube.com/@{}",
            "LinkedIn": "https://www.linkedin.com/in/{}/",
            "Facebook": "https://www.facebook.com/{}/",
            "TikTok": "https://www.tiktok.com/@{}",
            "Reddit": "https://www.reddit.com/user/{}/",
            "Snapchat": "https://www.snapchat.com/add/{}",
            "Tumblr": "https://{}.tumblr.com/",
            "Medium": "https://medium.com/@{}",
            "Dev.to": "https://dev.to/{}",
            "StackOverflow": "https://stackoverflow.com/users/{}/",
            "Quora": "https://www.quora.com/profile/{}",
            "SoundCloud": "https://soundcloud.com/{}",
            "Spotify": "https://open.spotify.com/user/{}",
            "Dribbble": "https://dribbble.com/{}",
            "Behance": "https://www.behance.net/{}",
            "Flickr": "https://www.flickr.com/people/{}/",
            "Vimeo": "https://vimeo.com/{}",
            "Discord": "https://discord.com/users/{}",
            "Telegram": "https://t.me/{}",
            "WhatsApp": "https://wa.me/{}",
            "Kaggle": "https://www.kaggle.com/{}",
            "ResearchGate": "https://www.researchgate.net/profile/{}",
            "Goodreads": "https://www.goodreads.com/user/show/{}",
            "ProductHunt": "https://www.producthunt.com/@{}",
            "Xing": "https://www.xing.com/profile/{}",
            "Weibo": "https://weibo.com/{}/",
            "VK": "https://vk.com/{}",
            "Mix": "https://mix.com/{}",
            "Patreon": "https://www.patreon.com/{}",
            "OnlyFans": "https://onlyfans.com/{}"
        }

        os.makedirs("logs", exist_ok=True)

    async def fetch(self, session, name, url_template, username):
        url = url_template.format(username)
        try:
            async with session.get(url, headers=self.headers, timeout=10) as response:
                content = await response.text()
                if response.status == 200 and "404" not in content and "not found" not in content.lower():
                    print(f"{Fore.GREEN}[+] {name:10} | ENCONTRADO: {url}")
                    
                    # Salva apenas o link em texto
                    filename = f"logs/{username}_links.txt"
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"[{name}] {url}\n")
                    
                    return {"rede": name, "url": url, "status": "Found", "logfile": filename}
                else:
                    return None
        except:
            return None

    async def scan(self, username):
        print(f"\n{Fore.CYAN} Iniciando varredura para: @{username}")
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, name, url, username) for name, url in self.targets.items()]
            results = await asyncio.gather(*tasks)
            return [r for r in results if r]

    async def google_dorking(self, username):
        dorks = [
            f'site:pastebin.com "{username}"',
            f'site:github.com "{username}"',
            f'site:linkedin.com "{username}"',
            f'site:twitter.com "{username}"',
            f'"{username}" filetype:pdf',
            f'"{username}" filetype:xls',
            f'"{username}" intitle:index.of'
        ]
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_google(session, dork, username) for dork in dorks]
            results = await asyncio.gather(*tasks)
            return [r for r in results if r]

    async def fetch_google(self, session, query, username):
        url = f"https://www.google.com/search?q={query}"
        try:
            async with session.get(url, headers=self.headers, timeout=10) as response:
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")
                links = [a["href"] for a in soup.select("a") if "http" in a.get("href", "")]
                if links:
                    print(f"{Fore.MAGENTA}[DORK] {query} → {len(links)} resultados")
                    
                    # Salva apenas os links encontrados
                    filename = f"logs/{username}_links.txt"
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"\n[DORK] {query}\n")
                        for link in links[:5]:
                            f.write(f"{link}\n")
                    
                    return {"query": query, "links": links[:5], "logfile": filename}
                return None
        except:
            return None


# Fluxo principal
async def main():
    print(Fore.BLUE + "=== CAIXA DE FERRAMENTAS CIBERSEGURANÇA: MÓDULO OSINT ===")
    conta_alvo = input("Digite o @ da conta: ").replace("@", "")
    
    scanner = CyberShieldOSINT()
    encontrados = await scanner.scan(conta_alvo)
    dorks = await scanner.google_dorking(conta_alvo)
    
    print(f"\n{Fore.YELLOW}Total de perfis suspeitos: {len(encontrados)}")
    print(f"{Fore.MAGENTA}Total de dorks processados: {len(dorks)}")
    print(f"{Fore.CYAN}Links salvos em: logs/{conta_alvo}_links.txt")
    return encontrados, dorks

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    resultados = loop.run_until_complete(main())