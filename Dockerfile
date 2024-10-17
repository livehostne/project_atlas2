FROM python:3.12-slim

WORKDIR /app
COPY . .

# Instala as dependências
RUN pip install -r requirements.txt

# Comando para rodar o bot
CMD ["python", "bot.py"]
