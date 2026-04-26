FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/

RUN pip install --no-cache-dir flask

RUN mkdir -p /data && chmod 755 /data

ENV API_URL=https://api.sosiva451.com/Avisos \
    OUTPUT_JSON=/data/output.json \
    OUTPUT_HTML=/data/output.html

EXPOSE 8080

CMD ["python", "server.py"]