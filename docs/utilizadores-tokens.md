# Utilizadores e tokens de teste

O middleware identifica o perfil **apenas** a partir de um token JWT assinado, enviado no cabeçalho `Authorization: Bearer <token>`. Parâmetros ou cabeçalhos do pedido (ex.: `?perfil=admin`) são ignorados.

Os tokens são emitidos por [`scripts/gerar_token.py`](../scripts/gerar_token.py), que simula o fornecedor de identidade. O middleware só os valida.

## Utilizadores

| `sub` | Perfil | Valor de `perfil` no token |
|---|---|---|
| `admin01` | Administrador | `administrador` |
| `analista01` | Operacional / Analista | `analista` |
| `publico01` | Público / Terceiros | `publico` |

Os valores de `perfil` coincidem com os de [`policies/politicas.yaml`](../policies/politicas.yaml).

## Formato do token

- **Algoritmo:** HS256. O middleware só aceita este algoritmo (rejeita `none` e outros).
- **Segredo:** variável de ambiente `JWT_SECRET`, nunca no código nem na configuração (ver [`.env.example`](../.env.example)).
- **Validade:** 60 minutos por defeito.

| Claim | Valor | Validado pelo middleware |
|---|---|---|
| `iss` | `apm-idp-teste` | Sim |
| `aud` | `adaptive-privacy-middleware` | Sim |
| `sub` | identificador do utilizador | Presente |
| `perfil` | `administrador`, `analista` ou `publico` | Sim, tem de existir na política |
| `iat` | data de emissão | — |
| `exp` | data de expiração | Sim |

Exemplo de payload:

```json
{
  "iss": "apm-idp-teste",
  "aud": "adaptive-privacy-middleware",
  "sub": "analista01",
  "perfil": "analista",
  "iat": 1795000000,
  "exp": 1795003600
}
```

## Gerar um token

```powershell
copy .env.example .env      # e substituir os valores
python scripts/gerar_token.py analista
python scripts/gerar_token.py publico --minutos 5
```

## Casos inválidos (para os testes de segurança)

| Caso | Resposta esperada |
|---|---|
| Sem cabeçalho `Authorization` | 401 |
| Token mal formado | 401 |
| Assinatura inválida (outro segredo) | 401 |
| Token expirado | 401 |
| Payload adulterado (ex.: `perfil` alterado sem nova assinatura) | 401 |
| Algoritmo `none` | 401 |
| `iss` ou `aud` errados | 401 |
| Token válido mas sem `perfil` ou com perfil desconhecido | 403 |

Em todos estes casos o middleware responde **sem contactar o backend**.
