# Etapa 1: Construir a aplicação Angular
FROM node:18 as build

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY package*.json ./
RUN npm install

COPY . .

# Construir a aplicação para produção
RUN npm run build --prod

# Etapa 2: Servir a aplicação com NGINX
FROM nginx:1.23

# Copiar os arquivos construídos para o diretório padrão do NGINX
COPY --from=build /app/dist/knowledge-extractor /usr/share/nginx/html

# Expor a porta padrão do NGINX
EXPOSE 80

# Comando para iniciar o servidor NGINX
CMD ["nginx", "-g", "daemon off;"]
