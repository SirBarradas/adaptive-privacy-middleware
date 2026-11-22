# Recurso de teste: `clientes`

## Cenário: Banco Exemplo

O **Banco Exemplo** (fictício) tem um sistema central com o registo de todos os clientes: é o **backend**. Várias equipas e entidades precisam destes dados, mas nenhuma precisa de todos. O **middleware** fica no meio e entrega a cada uma só o que lhe compete.

| Perfil | Quem é | Para que precisa dos dados | O que recebe |
|---|---|---|---|
| **Administrador** | Gestor de conta / back-office | Atender o cliente, corrigir dados | Tudo |
| **Analista** | Equipa de risco / marketing | Estudar padrões (saldo por região e idade) sem saber quem é quem | Registos individuais, sem nome nem morada, id pseudonimizado, NIF e email mascarados |
| **Público** | Parceiro externo / relatório público / entidade estatística | Estatísticas gerais | Só totais por distrito e faixa etária (grupos com menos de `k` clientes suprimidos) |

O recurso parte do registo de cliente da Tabela 5.1 do relatório da Parte 1 ([`report/part1/report.tex`](../report/part1/report.tex)), **alargado com a morada** (`morada`, `codigo_postal`, `concelho`) para mostrar a generalização hierárquica da localização:

```text
morada (rua, nº)  →  código postal (1000-123)  →  CP4 (1000) / concelho  →  distrito
   identifica                    quase identifica                              seguro para agregar
```

Todos os dados são **sintéticos**, gerados por [`backend/dados.py`](../backend/dados.py) (Faker `pt_PT`, semente fixa).

## Campos

| Campo | Tipo JSON | Formato / regra | Classe de sensibilidade |
|---|---|---|---|
| `id` | inteiro | Sequencial, a partir de 1 | Identificador direto |
| `nome` | string | Nome próprio e apelido | Identificador direto |
| `email` | string | Derivado do nome, domínio fictício `@exemplo.pt`; sufixo numérico se repetido | Identificador direto |
| `nif` | string | 9 dígitos, começa por 1 ou 2, dígito de controlo válido; string para preservar zeros e facilitar a mascaragem | Identificador direto |
| `data_nasc` | string | Data ISO `AAAA-MM-DD`; idade entre 18 e 90 anos a 2026-01-01 | Quase-identificador |
| `morada` | string | Rua e número (ex.: `Rua de Pinho, 12`) | Identificador direto |
| `codigo_postal` | string | `NNNN-NNN`, coerente com o concelho | Quase-identificador |
| `concelho` | string | Um dos concelhos da tabela do gerador (2 a 4 por distrito) | Quase-identificador |
| `distrito` | string | Um dos 18 distritos do continente ou uma das 2 regiões autónomas, coerente com o concelho | Quase-identificador |
| `saldo` | número | Decimal com 2 casas, ≥ 0; distribuição log-normal (mediana ≈ 1 100 €) | Atributo confidencial |

**Valores de `distrito`:** Aveiro, Beja, Braga, Bragança, Castelo Branco, Coimbra, Évora, Faro, Guarda, Leiria, Lisboa, Portalegre, Porto, Santarém, Setúbal, Viana do Castelo, Vila Real, Viseu, Região Autónoma dos Açores, Região Autónoma da Madeira.

Os clientes são distribuídos pelos distritos com pesos aproximados à população (Lisboa e Porto têm mais clientes). Com volumes pequenos (10 ou 100) haverá muitos distritos com poucos clientes. É intencional: permite testar a supressão de agregações abaixo do `k` mínimo.

## Exemplo de registo

```json
{
  "id": 1,
  "nome": "Joana Silva",
  "email": "joana.silva@exemplo.pt",
  "nif": "245678905",
  "data_nasc": "1987-03-14",
  "morada": "Rua de Pinho, 12",
  "codigo_postal": "1050-123",
  "concelho": "Lisboa",
  "distrito": "Lisboa",
  "saldo": 1520.75
}
```

## Transformação esperada por perfil

A política formal está em [`policies/politicas.yaml`](../policies/politicas.yaml) (tarefa 4).

| Campo | Administrador | Analista | Público |
|---|---|---|---|
| `id` | Manter | Pseudonimizar (`a91f…`) | Omitir |
| `nome` | Manter | Omitir | Omitir |
| `email` | Manter | Mascarar (`j***@exemplo.pt`) | Omitir |
| `nif` | Manter | Mascarar (`*****8905`) | Omitir |
| `data_nasc` | Manter | Generalizar (ano: `1987`) | Agregar (faixa etária) |
| `morada` | Manter | Omitir | Omitir |
| `codigo_postal` | Manter | Generalizar (CP4: `1050`) | Omitir |
| `concelho` | Manter | Manter | Omitir |
| `distrito` | Manter | Manter | Agregar (contagem) |
| `saldo` | Manter | Manter | Agregar (média por distrito) |

### O mesmo pedido, três respostas

```text
Administrador:  registo completo, como acima

Analista:       { "id": "a91f3c…", "email": "j***@exemplo.pt", "nif": "*****8905",
                  "data_nasc": "1987", "codigo_postal": "1050", "concelho": "Lisboa",
                  "distrito": "Lisboa", "saldo": 1520.75 }

Público:        { "clientes_por_distrito": { "Lisboa": 23, "Porto": 18, … },
                  "clientes_por_faixa_etaria": { "18-29": 15, "30-44": 31, … },
                  "saldo_medio_por_distrito": { "Lisboa": 2140.30, … } }
```

## API do backend

| Pedido | Resposta |
|---|---|
| `GET /clientes` | Lista completa (sem paginação: é o `S_orig`) |
| `GET /clientes/{id}` | Um cliente, ou 404 |

Todos os pedidos exigem o cabeçalho `X-Backend-Key` (ver [`backend/README.md`](../backend/README.md)).
