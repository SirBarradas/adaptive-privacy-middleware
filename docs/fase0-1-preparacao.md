# Fases 0 e 1 – Preparação e definições

Registo do que foi feito nas Fases 0 e 1 (tarefas 1 a 5 do [plano](../PLANO_PARTE2.md)), das decisões tomadas e porquê. Serve de base ao capítulo de implementação do relatório da Parte 2.

## Objetivo

Preparar o repositório e o ambiente (Fase 0) e fixar tudo o que o código vai precisar **antes de programar** (Fase 1): o recurso de teste, as políticas de privacidade e os utilizadores/tokens dos três perfis.

---

## Fase 0 – Preparação

### Tarefa 1 – Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `backend/` | API REST de teste com dados sintéticos |
| `middleware/` | Núcleo do middleware |
| `policies/` | Ficheiros de políticas |
| `tests/` | Testes `pytest` |
| `benchmarks/` | Scripts de benchmark e resultados (`results/`) |
| `docs/` | Documentação técnica e registos de cada fase |
| `scripts/` | Utilitários (ex.: gerar tokens) |
| `report/part1/`, `report/part2/` | Relatórios LaTeX da Parte 1 e da Parte 2 |

Cada pasta tem um `README.md` curto. `backend/`, `middleware/` e `tests/` são pacotes Python (`__init__.py`).

### Tarefa 2 – Ambiente

- **Python 3.13** (fixado em `.python-version`), com ambiente virtual `.venv` (fora do Git).
- Dependências com versões exatas em [`requirements.txt`](../requirements.txt):

| Pacote | Versão | Uso |
|---|---|---|
| FastAPI | 0.165.0 | API do backend e do middleware |
| Uvicorn | 0.54.0 | Servidor ASGI |
| httpx | 0.28.1 | Encaminhamento middleware → backend; clientes de benchmark |
| httpx2 | 2.16.2 | Cliente usado pelo `TestClient` nos testes |
| PyJWT | 2.15.1 | Tokens JWT |
| PyYAML | 6.0.4 | Leitura das políticas |
| python-dotenv | 1.2.4 | Leitura dos segredos do `.env` |
| Faker | 40.63.0 | Dados sintéticos |
| pytest | 9.2.0 | Testes |
| psutil | 7.2.2 | CPU e memória nos benchmarks |

- `pytest.ini` aponta os testes para `tests/`.
- `.gitignore` exclui ficheiros Python temporários, o `.venv` e os segredos (`.env`, `*.key`).

### Decisões da Fase 0

| Decisão | Alternativa considerada | Porquê |
|---|---|---|
| FastAPI | Flask | Suporte assíncrono nativo, útil para o encaminhamento com `httpx` e para os benchmarks com concorrência |
| Versões exatas (`==`) | Intervalos (`>=`) | Ambiente reprodutível entre os quatro elementos e na validação final (tarefa 25) |
| PyYAML, Faker, python-dotenv e httpx2 acrescentados à lista do plano | Só os pacotes listados no plano | Necessários para as políticas (YAML), os dados sintéticos, os segredos locais e para remover um aviso de descontinuação nos testes |
| Relatórios em `report/part1/` e `report/part2/` | Pasta única `report/` | O relatório da Parte 2 usa o mesmo template e fica ao lado do da Parte 1; nomes em inglês, como as restantes pastas |

---

## Fase 1 – Definições

### Tarefa 3 – Recurso de teste

O recurso `clientes` parte da Tabela 5.1 da Parte 1 e está descrito em [`recurso-clientes.md`](recurso-clientes.md), com:

- o cenário **Banco Exemplo** (fictício) e o papel de cada perfil;
- os campos, com tipo, formato e **classe de sensibilidade** (identificador direto, quase-identificador, atributo confidencial);
- um exemplo de registo e o exemplo "o mesmo pedido, três respostas".

Na Fase 2 o recurso foi alargado com `morada`, `codigo_postal` e `concelho` (ver [`fase2-backend.md`](fase2-backend.md)).

### Tarefa 4 – Políticas

Ficheiro [`policies/politicas.yaml`](../policies/politicas.yaml), documentado em [`policies/README.md`](../policies/README.md).

| Perfil | Modo | Resumo |
|---|---|---|
| `administrador` | `registos` | Todos os campos mantidos |
| `analista` | `registos` | `id` pseudonimizado; `nome` e `morada` omitidos; `email` e `nif` mascarados; `data_nasc` generalizada (ano); `codigo_postal` generalizado (CP4); `concelho`, `distrito` e `saldo` mantidos |
| `publico` | `agregado` (`k_min: 5`) | Contagem por distrito, contagem por faixa etária, saldo médio por distrito |

Regras gerais, a aplicar pelo motor de políticas (tarefa 10):

- campo não previsto na política → **omitido por defeito**;
- recurso ou perfil sem política, ou política inválida → **pedido recusado** (*fail-closed*);
- a chave da pseudonimização **não** está no ficheiro.

### Tarefa 5 – Utilizadores e tokens

Descrito em [`utilizadores-tokens.md`](utilizadores-tokens.md).

- Três utilizadores de teste: `admin01`, `analista01`, `publico01`.
- Tokens **JWT HS256** com `iss`, `aud`, `sub`, `perfil`, `iat` e `exp` (60 minutos).
- [`scripts/gerar_token.py`](../scripts/gerar_token.py) simula o fornecedor de identidade; o middleware só valida.
- Lista de casos inválidos com a resposta esperada (401/403), que servirá de base aos testes de segurança (tarefa 17).

### Segredos

Três chaves independentes, todas no `.env` local (fora do Git), com modelo em [`.env.example`](../.env.example):

| Variável | Uso |
|---|---|
| `JWT_SECRET` | Assinar e validar os tokens |
| `PSEUDONIM_KEY` | HMAC-SHA256 da pseudonimização |
| `BACKEND_KEY` | Chave partilhada middleware → backend (Fase 2) |

### Decisões da Fase 1

| Decisão | Alternativa considerada | Porquê |
|---|---|---|
| Políticas em YAML | JSON | Mais legível, permite comentários a justificar cada regra |
| Dois modos de perfil: `registos` e `agregado` | Ação `agregar` campo a campo | A agregação muda a forma da resposta (deixa de ser uma lista de registos), não se aplica a um campo isolado |
| `k_min = 5` | Outros valores (3, 10) | Valor comum na literatura de controlo de divulgação estatística; com 10 ou 100 registos suprime vários distritos, o que permite testar a supressão |
| Saldo médio **por distrito** | Média global | Mais utilidade para o perfil público; o `k_min` protege os distritos com poucos clientes |
| Omissão por defeito e *fail-closed* | Manter campos não previstos | Um campo novo no backend nunca é exposto por esquecimento (requisito da Parte 1) |
| Perfil extraído só do token | Parâmetro ou cabeçalho do pedido | Impede que o cliente escolha o próprio perfil (ex.: `?perfil=admin`) |
| JWT HS256 com `iss` e `aud` validados | RS256 (chave pública/privada) | Mais simples para um protótipo com um único emissor; `iss`/`aud` impedem reutilizar tokens de outros sistemas |
| Só HS256 aceite | Aceitar o algoritmo indicado no token | Evita o ataque `alg: none` e a confusão de algoritmos |
| Três segredos separados | Um segredo para tudo | Comprometer um não compromete os outros (ex.: quem obtém a `BACKEND_KEY` não consegue forjar tokens) |
| Script próprio para emitir tokens | Fornecedor de identidade real (Keycloak, etc.) | Fora do âmbito; o foco é o middleware |

## Limitações

- **HS256 é simétrico:** o emissor e o middleware partilham o mesmo segredo. Com RS256, o middleware só teria a chave pública e não conseguiria emitir tokens.
- Os tokens não podem ser revogados antes de expirarem e não existe *refresh*.
- Os segredos ficam em ficheiro `.env` local, sem cofre de segredos nem rotação.
- Os perfis são fixos (três), sem hierarquia nem atributos adicionais (ex.: finalidade declarada, que poderá entrar no R(t) da Fase 4).
