FROM python:3.9-slim

WORKDIR /app

# 1. Copia o arquivo de requisitos primeiro
COPY requirements.txt .

# 2. Instala as bibliotecas (AQUI que o gRPC é instalado)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia o restante do código (incluindo os arquivos .py gerados)
COPY . .

# Roda o script em modo "sem buffer" para vermos os logs na hora
CMD ["python", "-u", "isccp.py"]