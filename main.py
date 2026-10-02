import time
import requests
import yt_dlp

# COLE O LINK DO SEU CANAL AQUI ABAIXO
CANAL_URL = "https://www.youtube.com/@SEU_CANAL/videos"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
}

print(f"Buscando vídeos do canal: {CANAL_URL}\n")

# Configuração para pegar os links dos vídeos sem baixar o arquivo de vídeo
ydl_opts = {
    "extract_flat": True,
    "playlistend": 10,  # Pega os 10 vídeos mais recentes do canal
    "quiet": True,
}

urls_para_salvar = []

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(CANAL_URL, download=False)
        if "entries" in info:
            for entry in info["entries"]:
                video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                urls_para_salvar.append(video_url)

    print(f"Encontrados {len(urls_para_salvar)} vídeos recentes.\n")

    for url in urls_para_salvar:
        wayback_url = f"https://web.archive.org/save/{url}"
        print(f"Solicitando backup para: {url}")
        try:
            response = requests.get(wayback_url, headers=headers, timeout=30)
            if response.status_code == 200:
                print(f"[OK] Enviado com sucesso!")
            else:
                print(f"[!] Status {response.status_code}")
        except Exception as e:
            print(f"[X] Erro ao conectar: {e}")

        # Pausa de 10 segundos entre requisições
        time.sleep(10)

except Exception as e:
    print(f"Erro ao buscar o canal: {e}")

print("\nProcesso de backup concluído!")
