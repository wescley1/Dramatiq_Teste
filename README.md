# Dramatiq + RabbitMQ Demo

Este repositório contém um pequeno exemplo para aprender a usar Dramatiq com RabbitMQ.

Arquivos principais:

- `docker-compose.yml` - sobe um RabbitMQ local (porta 5672) com a UI em 15672.
- `dramatiq_project/tasks.py` - define a lógica dos tasks e os actors Dramatiq.
- `worker_a.py` / `worker_b.py` - scripts simples que iniciam workers distintos.
- `producer.py` - enfileira tarefas exemplares.
- `requirements.txt` - dependências Python.

Como executar (Windows PowerShell):

1) Subir RabbitMQ com docker-compose:

```powershell
docker compose up -d
```

2) Criar e ativar um ambiente virtual e instalar dependências:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

3) Em terminais separados, iniciar dois workers:

```powershell
python worker_a.py
```

```powershell
python worker_b.py
```

4) Enfileirar tarefas (em outro terminal):

```powershell
python producer.py
```

5) Ver o management UI: http://localhost:15672 (guest/guest)

Notas para uso empresarial:
- Nunca hardcode credenciais; use variáveis de ambiente ou um secret manager.
- Configure robustez: reconexão, limites de retries, dead-letter queues e monitoração.
- Use supervisores (systemd, docker, k8s) para garantir disponibilidade dos workers.
- Considere usar um pool de workers e particionamento de filas por responsabilidade.

Executando tudo em containers (isolado)
-------------------------------------

Se você encontrou problemas de conectividade host↔container (por exemplo, o
host não consegue se conectar ao RabbitMQ dentro do container), uma solução
conveniente é rodar os workers e o producer em containers na mesma rede do
RabbitMQ. Eu adicionei `Dockerfile` e `docker-compose.workers.yml` para isso.

Para subir RabbitMQ + 2 workers + um producer job (rodando uma vez):

```powershell
docker compose -f docker-compose.workers.yml up --build
```

O serviço `producer_once` roda `producer.py` uma vez e sai; os workers `worker_a`
e `worker_b` permanecem em execução e processam as mensagens.

Se preferir rodar apenas os workers em containers e executar o producer localmente,
use o mesmo `DRAMATIQ_BROKER_URL` apontando para `rabbitmq:5672` dentro de containers
ou para `127.0.0.1:5672` no host (workaround).

