FROM node:22-alpine
WORKDIR /app
COPY . .
RUN npm install --legacy-peer-deps
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh
EXPOSE 8545
CMD ["sh", "/app/run.sh"]