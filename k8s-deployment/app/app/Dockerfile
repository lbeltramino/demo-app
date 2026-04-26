FROM node:20-alpine
WORKDIR /app
COPY package.json .
COPY src/ ./src/
COPY public/ ./public/
EXPOSE 80
CMD ["node", "src/index.js"]
