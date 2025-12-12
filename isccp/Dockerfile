FROM python:3.9-slim

WORKDIR /app

# Copia o arquivo de requisitos primeiro
COPY requirements.txt .

# Instala as bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

CMD ["python", "-u", "isccp.py"]