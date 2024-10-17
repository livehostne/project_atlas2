# Usa uma imagem Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do bot e os arquivos necessários
COPY . .

# Exponha a porta que o Flask usará
EXPOSE 5000

# Comando para rodar o bot via gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
