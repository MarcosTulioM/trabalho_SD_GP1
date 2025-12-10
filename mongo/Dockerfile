FROM mongo:5.0

# Cria a chave usando um texto Base64 válido (Sem hifens, só letras e números)
# "VHJhYmFsaG9TREdQRjEyMDI1U2VjcmV0S2V5" é Base64 para "TrabalhoSDGPF12025SecretKey"
RUN echo "VHJhYmFsaG9TREdQRjEyMDI1U2VjcmV0S2V5" > /etc/mongo.key

# Aplica as permissões rigorosas (400) e dono (999 = mongodb user)
RUN chmod 400 /etc/mongo.key
RUN chown 999:999 /etc/mongo.key

# Inicia o banco
CMD ["mongod", "--replSet", "rs0", "--keyFile", "/etc/mongo.key", "--bind_ip_all"]