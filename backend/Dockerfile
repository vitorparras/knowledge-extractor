# Usar a imagem oficial do Python
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY . .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta do backend
EXPOSE 5001

# Comando para iniciar o backend
CMD ["python", "app.py"]
