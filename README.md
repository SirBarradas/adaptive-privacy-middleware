# adaptive-privacy-middleware

**Middleware Adaptativo de Privacidade e Redução de Dados em Sistemas de Informação**
Segurança de Redes e Sistemas de Informação – ISCTE

Middleware/proxy de segurança em Python que se coloca entre os clientes e um backend REST. Autentica cada pedido, identifica o perfil do utilizador a partir do token e aplica políticas de privacidade por recurso e perfil (manter, omitir, mascarar, pseudonimizar, generalizar, agregar) antes de devolver a resposta. Assim, cada perfil recebe apenas os dados de que precisa.

> ⚠️ O projeto usa apenas **dados sintéticos**.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| [`backend/`](backend/) | API REST de teste (`/clientes`) com dados sintéticos; só acessível pelo middleware |
| [`middleware/`](middleware/) | Núcleo do middleware: autenticação, encaminhamento, motor de políticas, transformadores, registo e métricas, componente adaptativo |
| [`policies/`](policies/) | Ficheiros de políticas (YAML/JSON) por recurso e perfil |
| [`tests/`](tests/) | Testes funcionais e de segurança (`pytest`) |
| [`benchmarks/`](benchmarks/) | Scripts de benchmark e resultados (CSV, tabelas, gráficos) |
| [`docs/`](docs/) | Documentação técnica: arquitetura, políticas, validação |
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
| Faker | Geração de dados sintéticos |
| pytest | Testes funcionais e de segurança |
| psutil | CPU e memória do middleware nos benchmarks |

## Execução

*A completar nas fases seguintes (ver [`PLANO_PARTE2.md`](PLANO_PARTE2.md)).*

## Testes

```powershell
pytest
```
