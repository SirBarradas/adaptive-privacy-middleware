# policies

Políticas de privacidade por recurso e perfil, em [`politicas.yaml`](politicas.yaml).

## Perfis

| Perfil | Valor no token | Modo |
|---|---|---|
| Administrador | `administrador` | `registos`: recebe os registos com os campos autorizados |
| Operacional / Analista | `analista` | `registos`: identificadores pseudonimizados, campos confidenciais mascarados ou omitidos |
| Público / Terceiros | `publico` | `agregado`: só recebe agregações, nunca registos individuais |

## Ações por campo (modo `registos`)

| Ação | Parâmetros | Exemplo |
|---|---|---|
| `manter` | — | `Lisboa` → `Lisboa` |
| `omitir` | — | campo removido |
| `mascarar` | `manter_inicio`, `manter_fim`, `manter_dominio` | `245678905` → `*****8905` |
| `pseudonimizar` | — (HMAC-SHA256, chave em variável de ambiente) | `1` → `a91f…` |
| `generalizar` | `nivel` (ex.: `ano`) | `1987-03-14` → `1987` |

## Agregações (modo `agregado`)

Cada agregação tem `nome`, `funcao` (`contagem` ou `media`), `agrupar_por` e, para `media`, o `campo`. Os grupos com menos de `k_min` registos são suprimidos.

## Regras gerais

- Campos não previstos na política são **omitidos por defeito**.
- Recurso ou perfil sem política, ou política inválida → **pedido recusado** (*fail-closed*).
- Nunca guardar aqui chaves nem segredos.
