# Usa a imagem oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos da aplicação para o container
COPY . .

# Define a variável de ambiente para o token do bot (pode ser configurado na Render)
ENV TOKEN=${TOKEN}

# Expõe a porta (não necessário para bots Telegram, mas pode ser útil se precisar de webhook)
# EXPOSE 8443

# Comando para iniciar o bot
CMD ["python", "bot.py"]
