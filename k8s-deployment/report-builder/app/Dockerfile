FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/

RUN pip install --no-cache-dir flask

RUN mkdir -p /data && chmod 755 /data

ENV API_URL=https://api.sosiva451.com/Avisos \
    DATA_DIR=/data

EXPOSE 8080

CMD ["python", "-u", "server.py"]