import requests
import time

# =========================================================
# CONFIGURAÇÕES PESSOAIS DO HEVERTON
# =========================================================
TOKEN_TELEGRAM = "8281833655:AAFOvs0EOPw2XPXtLYFcWbVg_T9J9Mo8aqM"
CHAT_ID = "1184648405"
API_KEY_FUTEBOL = "c0b8e7b4bamsh38fe431bf2ece40p10c28fjsnc28aea35bfeb"
# =========================================================

def enviar_mensagem_telegram(mensagem):
    """Função para enviar os alertas diretamente para o seu Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    dados = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=dados)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def buscar_jogos_e_analisar():
    """Função que consulta a API e filtra as melhores oportunidades"""
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"live": "all"} # Busca apenas jogos que estão acontecendo AGORA
    
    headers = {
        "X-RapidAPI-Key": API_KEY_FUTEBOL,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        print(f"[{time.strftime('%H:%M:%S')}] Iniciando varredura nos jogos ao vivo...")
        response = requests.get(url, headers=headers, params=querystring).json()
        jogos = response.get('response', [])

        if not jogos:
            print("Nenhum jogo ao vivo encontrado no momento.")
            return

        for jogo in jogos:
            time_casa = jogo['teams']['home']['name']
            time_fora = jogo['teams']['away']['name']
            gols_casa = jogo['goals']['home']
            gols_fora = jogo['goals']['away']
            minuto = jogo['fixture']['status']['elapsed']

            # -----------------------------------------------------------
            # ESTRATÉGIA: LAY CORRECT SCORE (CONTRA O 0-0)
            # Alerta se o jogo estiver 0x0 entre os minutos 20 e 35
            # -----------------------------------------------------------
            if 20 <= minuto <= 35 and gols_casa == 0 and gols_fora == 0:
                alerta = (
                    f"🔥 *OPORTUNIDADE: LAY 0-0*\n\n"
                    f"🏟 *Jogo:* {time_casa} x {time_fora}\n"
                    f"⏰ *Tempo:* {minuto}' minutos\n"
                    f"⚽ *Placar:* {gols_casa}x{gols_fora}\n\n"
                    f"💡 *Sugestão:* O mercado de 0x0 está segurando a odd. "
                    f"Chance alta de sair um gol ainda no primeiro tempo!"
                )
                enviar_mensagem_telegram(alerta)
                print(f"✅ Alerta enviado para: {time_casa} x {time_fora}")
                time.sleep(2) # Pausa curta para não ser bloqueado pelo Telegram

    except Exception as e:
        print(f"Erro na varredura: {e}")

# --- COMANDO PRINCIPAL (O QUE LIGA O BOT) ---

if __name__ == "__main__":
    print("Iniciando Robô de Trade do Heverton...")
    enviar_mensagem_telegram("🚀 *ROBÔ DO HEVERTON ATIVADO!*\n\nMonitorando jogos ao vivo 24h por dia.")
    
    while True:
        buscar_jogos_e_analisar()
        # O robô descansa 10 minutos (600 segundos) entre as consultas
        # Isso serve para não esgotar o seu plano gratuito da API RapidAPI
        time.sleep(600)
