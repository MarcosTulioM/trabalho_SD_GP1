🎯 Objetivo
Desenvolvimento de um sistema distribuído robusto para coleta, processamento, armazenamento persistente e visualização de dados de sensores de carros de Fórmula 1 (pressão, temperatura e desgaste dos pneus). O sistema utiliza contêineres para orquestração e implementa múltiplos padrões de comunicação.

🏗️ Arquitetura do Sistema
O projeto foi dividido em quatro subsistemas principais, todos rodando em Docker Containers orquestrados pelo Docker Compose:

1. Subsistema de Coleta (SCCP - Carros)
Componente: carro

Função: Simula os sensores dos carros. Gera dados aleatórios de telemetria em tempo real.

Protocolo: MQTT (Assíncrono/PubSub).

Fluxo: Publica JSON no tópico f1/carro{id}/pneus no Broker Mosquitto.

2. Subsistema de Intermediação e Armazenamento (SACP)
Este subsistema é dividido em duas partes que conversam entre si:

A. Coletor (ISCCP):

Função: Ouve o Broker MQTT. Atua como um "Tradutor/Gateway".

Ação: Recebe a mensagem MQTT, converte para um objeto Protobuf e envia para o servidor de armazenamento.

Protocolo: Cliente gRPC.

B. Armazenamento (SSACP):

Função: Recebe os dados estruturados e gerencia a conexão com o banco de dados.

Ação: Persiste os dados recebidos no Cluster MongoDB.

Protocolo: Servidor gRPC.

3. Persistência de Dados (Cluster MongoDB)
Componentes: mongo1, mongo2, mongo3.

Arquitetura: ReplicaSet (1 Primário, 2 Secundários) para alta disponibilidade e tolerância a falhas.

Segurança: Autenticação ativada (User/Pass) e comunicação interna segura via KeyFile (gerado em imagem customizada para evitar problemas de permissão do host).

4. Subsistema de Visualização (SVCP)
Componente: ssvcp

Tecnologia: FastAPI (Python).

Função: Expõe os dados armazenados para consumo externo.

Protocolo: REST API (HTTP).

Acesso: Disponibiliza endpoints JSON em http://localhost:8000/pneus.

🔄 Fluxo de Dados (Pipeline)
Geração: O Carro gera o dado {pressao: 30.5}.

Envio: Envia via MQTT para o Broker.

Tradução: O ISCCP consome o tópico, cria um objeto DadosPneu (gRPC).

Transmissão: O ISCCP chama o método remoto EnviarDadosPneu no SSACP.

Persistência: O SSACP grava o documento no MongoDB (Primary).

Replicação: O MongoDB replica o dado para os nós secundários.

Consumo: O usuário acessa o navegador, o SSVCP consulta o banco e devolve o JSON.

🛠️ Tecnologias e Desafios Superados
Docker & Docker Compose: Orquestração de 9 containers simultâneos (mongo1-3, isccp1-2, carro1-2, ssacp, ssvcp, broker).

Protocol Buffers (Protobuf): Definição estrita da estrutura de dados (.proto) garantindo contrato firme entre cliente e servidor.

gRPC: Implementação de comunicação remota de alta performance.

MongoDB ReplicaSet: Configuração avançada de cluster com autenticação e resolução de problemas de permissão de arquivos (KeyFile) no Windows.

FastAPI: Criação de uma API moderna e assíncrona.

🚀 Como Executar
Iniciar o sistema:

docker-compose up -d

(O sistema sobe, configura a rede, inicia o cluster de banco e começa a processar dados automaticamente).

Visualizar os dados: Acessar: http://localhost:8000/pneus

Parar o sistema:

docker-compose down