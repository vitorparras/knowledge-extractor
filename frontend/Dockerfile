# Base image
FROM node:16

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application files
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 8080

# Start the application
CMD ["npm", "run", "serve"]
