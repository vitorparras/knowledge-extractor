# Usando a imagem oficial do Python
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários
COPY requirements.txt .
COPY . .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
