FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install "paho-mqtt<2.0.0"
CMD ["python", "carro.py"]