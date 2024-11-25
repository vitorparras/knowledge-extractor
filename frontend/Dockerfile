FROM node:18-alpine
WORKDIR /app

# Copiar os arquivos de dependência e instalar
COPY package.json package-lock.json ./
RUN npm install

# Copiar o restante do código do frontend
COPY . .

# Expor a porta padrão do Angular CLI
EXPOSE 4200

# Adicionar --host=0.0.0.0 ao comando de inicialização
CMD ["npm", "start", "--", "--host=0.0.0.0", "--disable-host-check"]


