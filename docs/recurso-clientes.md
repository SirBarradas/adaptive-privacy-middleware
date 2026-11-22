# Recurso de teste: `clientes`

Recurso usado pelo backend de teste e protegido pelo middleware. Corresponde ao registo de cliente da Tabela 5.1 do relatório da Parte 1 ([`report/part1/report.tex`](../report/part1/report.tex)).

Todos os dados são **sintéticos** (gerados com Faker, locale `pt_PT`, seed fixa para reprodutibilidade).

## Campos

| Campo | Tipo JSON | Formato / regra | Classe de sensibilidade |
|---|---|---|---|
| `id` | inteiro | Sequencial, a partir de 1 | Identificador direto |
| `nome` | string | Nome próprio e apelido | Identificador direto |
| `email` | string | Derivado do nome, domínio fictício `@exemplo.pt` | Identificador direto |
| `nif` | string | 9 dígitos com dígito de controlo válido; string para preservar zeros à esquerda e facilitar a mascaragem | Identificador direto |
| `data_nasc` | string | Data ISO `AAAA-MM-DD`; idade entre 18 e 90 anos | Quase-identificador |
| `distrito` | string | Um dos 18 distritos do continente ou uma das 2 regiões autónomas (lista abaixo) | Quase-identificador |
| `saldo` | número | Decimal com 2 casas, ≥ 0; distribuição assimétrica (muitos saldos baixos, poucos altos) | Atributo confidencial |

**Valores de `distrito`:** Aveiro, Beja, Braga, Bragança, Castelo Branco, Coimbra, Évora, Faro, Guarda, Leiria, Lisboa, Portalegre, Porto, Santarém, Setúbal, Viana do Castelo, Vila Real, Viseu, Região Autónoma dos Açores, Região Autónoma da Madeira.

> Com volumes pequenos (10 ou 100 registos) haverá muitos distritos com poucos clientes. Isto é intencional: permite testar a supressão de agregações abaixo do `k` mínimo.

## Exemplo de registo

```json
{
  "id": 1,
  "nome": "Joana Silva",
  "email": "joana.silva@exemplo.pt",
  "nif": "245678905",
  "data_nasc": "1987-03-14",
  "distrito": "Lisboa",
  "saldo": 1520.75
}
```

## Transformação esperada por perfil

Resumo da Tabela 5.1. A política formal é definida na tarefa 4, em [`policies/`](../policies/).

| Campo | Administrador | Operacional / Analista | Público / Terceiros |
|---|---|---|---|
| `id` | Manter | Pseudonimizar | Omitir |
| `nome` | Manter | Omitir | Omitir |
| `email` | Manter | Mascarar (`j***@exemplo.pt`) | Omitir |
| `nif` | Manter | Mascarar (`*****8905`) | Omitir |
| `data_nasc` | Manter | Generalizar (ano) | Agregar (faixa etária) |
| `distrito` | Manter | Manter | Agregar (contagem) |
| `saldo` | Manter | Manter | Agregar (média) |
