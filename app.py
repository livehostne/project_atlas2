import os
import json
import requests
import telebot
import time
from flask import Flask
from telegraph import Telegraph

# Substitua pelo seu token do bot do Telegram
TOKEN = '6924758966:AAGUnrEbkpHL-5q127lZN3G7RJwsboiHpOs'
DB_FOLDER = 'db'  # Pasta onde estão os arquivos JSON

# Inicializa o bot do Telegram
bot = telebot.TeleBot(TOKEN)

# Inicializa o Telegraph
telegraph = Telegraph()
telegraph.create_account(short_name='Game Library')

# Função para carregar arquivos JSON da pasta 'db'
def load_json_files():
    all_games = []
    json_files = [f for f in os.listdir(DB_FOLDER) if f.endswith('.json')]
    
    for index, filename in enumerate(json_files):
        file_path = os.path.join(DB_FOLDER, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_games.extend(data['downloads'])
        except Exception as e:
            print(f"Erro ao ler {filename}: {e}")
    
    return all_games, len(json_files)

# Função para filtrar jogos com base no termo de busca
def filter_games(search_term, games_data):
    return [game for game in games_data if search_term.lower() in game['title'].lower()]

# Função para encurtar URLs usando TinyURL
def encurtar_url(url):
    api_url = f"http://tinyurl.com/api-create.php?url={url}"
    response = requests.get(api_url)
    return response.text if response.status_code == 200 else url

# Função para exibir barra de progresso
def atualizar_barra_progresso(message, total, progresso):
    barra = '▰' * progresso + '▱' * (total - progresso)
    texto = f"🔍 Buscando jogos...\n[{barra}] {progresso}/{total}"
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto)

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bem-vindo à Game Library! Use /buscar <nome_do_jogo> para procurar por um jogo.")

# Comando /buscar
@bot.message_handler(commands=['buscar'])
def buscar_jogo(message):
    search_term = message.text.replace('/buscar', '').strip()

    if not search_term:
        bot.reply_to(message, "Por favor, forneça o nome de um jogo para buscar. Exemplo: /buscar Skyrim")
        return

    # Envia mensagem inicial com barra de progresso vazia
    progresso_message = bot.reply_to(message, "🔍 Buscando jogos...\n[▱▱▱▱▱▱▱▱▱▱] 0/0")
    
    games_data, total_files = load_json_files()  # Carrega todos os jogos da pasta db
    
    # Simula carregamento de arquivos com barra de progresso
    for i in range(1, 11):
        time.sleep(0.8)  # Simulação de progresso (ajuste conforme necessário)
        atualizar_barra_progresso(progresso_message, 10, i)

    # Filtra jogos com base no termo de busca
    filtered_games = filter_games(search_term, games_data)

    if filtered_games:
        # Cria a página no Telegraph com um layout mais bonito usando apenas tags permitidas
        title = f"🎮 Resultados para '{search_term}'"
        content = f"""
        <b>⚠️ AVISO IMPORTANTE</b><br>
        <i>Por favor, tenha um cliente torrent instalado antes de fazer o download!</i><br><br>
        <b>Encontramos {len(filtered_games)} resultado(s) para "<i>{search_term}</i>":</b><br><br>
        <ul>"""

        for game in filtered_games:
            title = game['title']
            download_link = encurtar_url(game['uris'][0])  # Encurtar o link do download

            # Melhor design para cada jogo listado
            content += f"""
            <li><b>{title}</b>: <a href='{download_link}'>🔗 Download Link</a></li>"""

        content += "</ul>"

        # Publica a página no Telegraph
        page = telegraph.create_page(
            title=title,
            html_content=content
        )

        # Envia o link da página criada
        bot.edit_message_text(chat_id=message.chat.id, message_id=progresso_message.message_id, text=f"Aqui estão os resultados: {page['url']}")
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=progresso_message.message_id, text=f"Nenhum jogo encontrado para '{search_term}'.")

# Função para lidar com mensagens não reconhecidas
@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    bot.reply_to(message, "Desculpe, não entendi esse comando. Tente usar /buscar <nome_do_jogo>.")

# Iniciar o bot
def start_bot():
    bot.polling()

# Inicializa o Flask para manter o bot ativo
app = Flask(__name__)

@app.route('/')
def index():
    return "O bot está rodando!"

if __name__ == '__main__':
    start_bot()
