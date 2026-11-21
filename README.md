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

## Instalação e execução

*A completar nas fases seguintes (ver [`PLANO_PARTE2.md`](PLANO_PARTE2.md)).*
