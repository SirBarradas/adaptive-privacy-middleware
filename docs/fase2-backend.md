# Fase 2 – Backend de teste

Registo do que foi feito na Fase 2 (tarefas 6 e 7 do [plano](../PLANO_PARTE2.md)), das decisões tomadas e porquê. Serve de base ao capítulo de implementação do relatório da Parte 2.

## Objetivo

Construir o sistema que o middleware vai proteger: uma API REST simples com dados sintéticos de clientes, que **só aceita pedidos do middleware**.

## Cenário

O backend representa o sistema central de clientes do **Banco Exemplo** (fictício). Os consumidores (administrador, analista, público) nunca falam diretamente com ele: passam sempre pelo middleware. Detalhes em [`recurso-clientes.md`](recurso-clientes.md).

## O que foi implementado

| Ficheiro | Conteúdo |
|---|---|
| [`backend/dados.py`](../backend/dados.py) | Gerador de clientes sintéticos |
| [`backend/app.py`](../backend/app.py) | API REST (FastAPI) |
| [`tests/test_backend.py`](../tests/test_backend.py) | 22 testes automáticos (`pytest`) |

### Tarefa 6 – API REST com dados sintéticos

**Endpoints:**

| Pedido | Resposta |
|---|---|
| `GET /clientes` | Lista completa de clientes |
| `GET /clientes/{id}` | Um cliente, ou 404 |

**Dados gerados** (Faker `pt_PT`, semente fixa `42`):

- 10 campos: `id`, `nome`, `email`, `nif`, `data_nasc`, `morada`, `codigo_postal`, `concelho`, `distrito`, `saldo`.
- **NIF** de 9 dígitos com dígito de controlo válido (módulo 11).
- **Email** derivado do nome, em domínio fictício `@exemplo.pt`, sem repetições (sufixo numérico quando há nomes iguais).
- **Idade** entre 18 e 90 anos, calculada a partir de uma data de referência fixa (2026-01-01), para que os dados não mudem com o dia em que são gerados.
- **Localização coerente:** cerca de 50 concelhos (2 a 4 por distrito), cada um com o seu código postal base. O concelho e o código postal batem sempre certo com o distrito.
- **Distritos com pesos aproximados à população** (Lisboa e Porto com mais clientes, Portalegre com menos).
- **Saldo** com distribuição log-normal (muitos saldos baixos, poucos altos; mediana ≈ 1 100 €).

**Volume configurável** pela variável `BACKEND_N_REGISTOS` (10, 100, 1 000 ou 10 000).

### Tarefa 7 – Acesso só a partir do middleware

Duas camadas de proteção:

| Camada | Implementação | O que impede |
|---|---|---|
| Rede | Servidor escuta apenas em `127.0.0.1:8001` | Acesso a partir de outras máquinas |
| Chave partilhada | Cabeçalho `X-Backend-Key` comparado com `BACKEND_KEY` em tempo constante (`hmac.compare_digest`) | Acesso de outros processos na mesma máquina |

Medidas adicionais:

- **Fail-closed:** sem `BACKEND_KEY` definida, o backend recusa-se a arrancar.
- A verificação da chave é feita num *middleware* HTTP, por isso cobre **todos** os caminhos, incluindo os inexistentes (um atacante sem chave nem consegue saber que caminhos existem).
- Respostas de erro genéricas (`{"erro": "Não autorizado"}`), sem detalhes internos.
- Documentação automática do FastAPI desativada (`/docs`, `/redoc`, `/openapi.json`).
- Cabeçalho `server` removido das respostas.

## Decisões e justificação

| Decisão | Alternativa considerada | Porquê |
|---|---|---|
| Recurso alargado com `morada`, `codigo_postal` e `concelho` (a Tabela 5.1 da Parte 1 só tinha `distrito`) | Manter só o distrito | Num sistema real a ficha guarda a morada completa. Permite mostrar a generalização hierárquica (morada → código postal → CP4/concelho → distrito), torna mais visível a descida de entropia H(X) e o efeito do `k` mínimo, e aumenta o ∆D |
| Dados gerados uma vez no arranque e lista serializada uma só vez | Gerar a cada pedido | Os benchmarks devem medir o custo do middleware, não o da geração de dados |
| Sem paginação em `GET /clientes` | Paginação | A resposta completa é o `S_orig` a comparar com o `S_trans` |
| Volume definido por variável de ambiente no arranque | Parâmetro no pedido (`?n=`) | Nenhum cliente consegue alterar os dados a partir do pedido |
| Chave partilhada | mTLS | Muito mais simples e suficiente para um protótipo; o mTLS fica como limitação/trabalho futuro |
| Semente fixa | Dados aleatórios a cada arranque | Testes e benchmarks reprodutíveis; os primeiros *k* clientes são iguais para qualquer volume |
| Backend guarda o `distrito` (não é calculado pelo middleware a partir do concelho) | Middleware com tabela geográfica | Mantém o middleware genérico, sem conhecimento do domínio |

**Ligação com a Fase 6 (benchmarks):** o cenário "acesso direto" envia a chave diretamente ao backend, simulando um sistema sem camada de privacidade, sem ser preciso abrir uma porta traseira no backend.

## Testes

22 testes automáticos, todos a passar (`pytest tests/test_backend.py -v`):

| Teste | O que verifica | N.º |
|---|---|---|
| `test_volume` | Cada volume (10, 100, 1 000, 10 000) devolve exatamente *n* registos | 4 |
| `test_esquema_e_regras` | 10 campos, NIF válido, email único, distrito na lista, concelho coerente com o distrito, código postal `NNNN-NNN`, idade 18–90, saldo ≥ 0 com 2 casas | 1 |
| `test_reprodutivel` | Mesma semente → mesmos dados; os primeiros registos não dependem do volume | 1 |
| `test_obter_cliente` | `GET /clientes/{id}` devolve o cliente certo; id inexistente → 404 | 1 |
| `test_sem_documentacao_exposta` | `/docs`, `/redoc`, `/openapi.json` → 404 | 1 |
| `test_json_declara_utf8` | Todas as respostas (incluindo erros) declaram `charset=utf-8` | 4 |
| `test_rejeita_sem_chave_valida` | Sem chave, chave errada ou chave quase certa → 401, em `/clientes`, `/clientes/1` e caminhos inexistentes | 9 |
| `test_nao_arranca_sem_chave` | Sem `BACKEND_KEY`, a aplicação não arranca | 1 |

Os testes usam o `TestClient` do FastAPI, sem precisar de servidor a correr. O teste de rejeição sem chave antecipa um dos pontos da tarefa 17 (Fase 5: "o backend não é acessível diretamente").

**Verificação manual com o servidor a correr:** sem chave → 401; com chave → dados; `netstat` confirma que só escuta em `127.0.0.1:8001`.

## Problemas encontrados e correções

| Problema | Causa | Correção |
|---|---|---|
| Nomes com acentos errados no PowerShell (`InÃªs` em vez de `Inês`) | As respostas declaravam `application/json` sem `charset`; o Windows PowerShell 5.1 assume ISO-8859-1 | Todas as respostas passaram a declarar `application/json; charset=utf-8`; acrescentado teste |
| Aviso `StarletteDeprecationWarning` nos testes | O `TestClient` do Starlette vai deixar de usar o `httpx` | Instalado o `httpx2` (adotado automaticamente pelo Starlette) em vez de esconder o aviso |

## Limitações

- A proteção por rede (`127.0.0.1`) só funciona com middleware e backend na mesma máquina. Em máquinas separadas seria preciso uma rede interna (ex.: rede Docker na tarefa 26) ou firewall.
- A chave partilhada não cifra o tráfego: entre middleware e backend a comunicação é HTTP simples. Em produção seria necessário TLS (ou mTLS).
- A chave é estática, sem rotação.
- Os dados sintéticos são plausíveis mas não estatisticamente representativos da população portuguesa (a tabela de concelhos é parcial).

## Como reproduzir

```powershell
.venv\Scripts\Activate.ps1
pytest tests/test_backend.py -v          # testes
python -m backend.app                    # backend em 127.0.0.1:8001
```

Pedidos de exemplo em [`backend/README.md`](../backend/README.md).
