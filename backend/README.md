# backend

Backend de teste: o sistema central de clientes do **Banco Exemplo** (fictício), com dados sintéticos. Esquema e cenário em [`docs/recurso-clientes.md`](../docs/recurso-clientes.md).

| Ficheiro | Conteúdo |
|---|---|
| [`dados.py`](dados.py) | Gerador de clientes sintéticos (Faker `pt_PT`, semente fixa, reprodutível) |
| [`app.py`](app.py) | API REST: `GET /clientes`, `GET /clientes/{id}` |

## Executar

A partir da raiz do repositório, com o `.env` configurado (ver [`.env.example`](../.env.example)):

```powershell
python -m backend.app
```

| Variável | Por defeito | Significado |
|---|---|---|
| `BACKEND_KEY` | — (obrigatória) | Chave partilhada com o middleware |
| `BACKEND_N_REGISTOS` | `100` | N.º de clientes gerados no arranque (10, 100, 1000, 10000) |
| `BACKEND_HOST` | `127.0.0.1` | Interface onde escuta |
| `BACKEND_PORT` | `8001` | Porta |

Os dados são gerados uma vez no arranque e a lista é serializada uma só vez, para que os benchmarks meçam o middleware e não o backend. Para mudar o volume, reiniciar com outro `BACKEND_N_REGISTOS`.

## Acesso só pelo middleware

Duas camadas:

1. **Rede:** escuta apenas em `127.0.0.1`, por isso não é acessível a partir de outras máquinas.
2. **Chave partilhada:** todos os pedidos (incluindo caminhos inexistentes) exigem o cabeçalho `X-Backend-Key` igual a `BACKEND_KEY`, comparado em tempo constante. Sem a chave, a resposta é `401 {"erro": "Não autorizado"}`, sem detalhes internos.

Também não arranca sem `BACKEND_KEY` (*fail-closed*), não expõe `/docs` nem `/openapi.json` e não envia o cabeçalho `server`.

No benchmark "acesso direto vs. middleware" (Fase 6), o cenário direto envia a chave diretamente ao backend, simulando um sistema sem camada de privacidade.
