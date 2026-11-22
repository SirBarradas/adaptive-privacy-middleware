# adaptive-privacy-middleware

**Middleware Adaptativo de Privacidade e Redução de Dados em Sistemas de Informação**
Segurança de Redes e Sistemas de Informação – ISCTE

Middleware/proxy de segurança em Python que se coloca entre os clientes e um backend REST. Autentica cada pedido, identifica o perfil do utilizador a partir do token e aplica políticas de privacidade por recurso e perfil (manter, omitir, mascarar, pseudonimizar, generalizar, agregar) antes de devolver a resposta. Assim, cada perfil recebe apenas os dados de que precisa.

> ⚠️ O projeto usa apenas **dados sintéticos**.

## Cenário

O **Banco Exemplo** (fictício) guarda o registo dos seus clientes num sistema central (o backend). Três tipos de consumidores pedem os mesmos dados, e o middleware entrega a cada um só o que lhe compete:

- **Administrador** (gestor de conta): registo completo;
- **Analista** (equipa de risco/marketing): registos sem nome nem morada, com identificadores pseudonimizados e campos sensíveis mascarados ou generalizados;
- **Público** (parceiros, estatísticas): apenas totais agregados, sem grupos com menos de `k` clientes.

Detalhes em [`docs/recurso-clientes.md`](docs/recurso-clientes.md).

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| [`backend/`](backend/) | API REST de teste (`/clientes`) com dados sintéticos; só acessível pelo middleware |
| [`middleware/`](middleware/) | Núcleo do middleware: autenticação, encaminhamento, motor de políticas, transformadores, registo e métricas, componente adaptativo |
| [`policies/`](policies/) | Ficheiros de políticas (YAML/JSON) por recurso e perfil |
| [`tests/`](tests/) | Testes funcionais e de segurança (`pytest`) |
| [`benchmarks/`](benchmarks/) | Scripts de benchmark e resultados (CSV, tabelas, gráficos) |
| [`docs/`](docs/) | Documentação técnica: arquitetura, políticas, validação |
| [`scripts/`](scripts/) | Utilitários (ex.: gerar tokens JWT de teste) |
| [`report/part1/`](report/part1/) | Relatório da Parte 1 (teórica), em LaTeX |
| [`report/part2/`](report/part2/) | Relatório da Parte 2 (prática), em LaTeX |
| [`PLANO_PARTE2.md`](PLANO_PARTE2.md) | Plano de tarefas da Parte 2 (prática) |

## Instalação

Requer **Python 3.13**. A partir da raiz do repositório:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

| Pacote | Uso |
|---|---|
| FastAPI + Uvicorn | API do backend de teste e do middleware |
| httpx | Encaminhamento middleware → backend; clientes de teste e benchmark |
| PyJWT | Validação dos tokens e extração do perfil |
| PyYAML | Leitura dos ficheiros de políticas |
| python-dotenv | Leitura dos segredos locais do `.env` |
| Faker | Geração de dados sintéticos |
| pytest | Testes funcionais e de segurança |
| psutil | CPU e memória do middleware nos benchmarks |

## Configuração

Copiar o modelo e substituir os valores por segredos aleatórios (`python -c "import secrets; print(secrets.token_hex(32))"`):

```powershell
copy .env.example .env
```

O `.env` nunca vai para o Git.

## Execução

**Backend de teste** (escuta em `127.0.0.1:8001`; ver [`backend/README.md`](backend/README.md)):

```powershell
python -m backend.app
```

**Middleware:** *a completar na Fase 3.*

## Testes

```powershell
pytest
```
