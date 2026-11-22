# Plano de Tarefas – Projeto Parte 2 (Prática)

**Middleware Adaptativo de Privacidade e Redução de Dados em Sistemas de Informação**
Segurança de Redes e Sistemas de Informação – ISCTE

> **Como usar este ficheiro**
> - Marcar uma tarefa como concluída trocando `[ ]` por `[x]` (no GitHub também se pode clicar na caixa ao editar no browser).
> - Fazer commit da atualização deste ficheiro sempre que uma tarefa for fechada.
> - Respeitar a ordem das fases: cada uma depende da anterior.


---

## Cotação da Parte 2 (20 valores)

| Componente | Valores | Fases relacionadas |
|---|---|---|
| Implementação | 8 | 2, 3, 4 |
| Testes e comparativos práticos de resultados | 6 | 5, 6 |
| Validação do protótipo | 4 | 7 |
| Relatório / Vídeo de apresentação | 2 | 8, 9 |

---

## Progresso geral

- [x] Fase 0 – Preparação
- [ ] Fase 1 – Definições
- [ ] Fase 2 – Backend de teste
- [ ] Fase 3 – Núcleo do middleware
- [ ] Fase 4 – Componente adaptativo
- [ ] Fase 5 – Testes funcionais e de segurança
- [ ] Fase 6 – Benchmarks e comparativos
- [ ] Fase 7 – Validação do protótipo
- [ ] Fase 8 – Repositório e reprodutibilidade
- [ ] Fase 9 – Relatório e vídeo

---

## Fase 0 – Preparação

- [x] **1.** Criar o repositório GitHub com a estrutura `backend/`, `middleware/`, `policies/`, `tests/`, `benchmarks/`, `docs/` e um README inicial.
- [x] **2.** Fixar o ambiente: versão do Python, FastAPI (ou Flask), `httpx`, `pytest`, `psutil`, `PyJWT` e ficheiro `requirements.txt`.


## Fase 1 – Definições (antes de programar)

- [ ] **4.** Fixar o recurso de teste: registo de clientes da Tabela 5.1 (`id`, `nome`, `email`, `nif`, `data_nasc`, `distrito`, `saldo`).
- [ ] **5.** Escrever o ficheiro de políticas (YAML/JSON) por recurso e perfil, com a ação para cada campo (manter, omitir, mascarar, pseudonimizar, generalizar, agregar) e o tamanho mínimo de grupo `k` para agregações.
- [ ] **6.** Definir os utilizadores e tokens de teste para os três perfis (Administrador, Operacional/Analista, Público/Terceiros).

## Fase 2 – Backend de teste

- [ ] **7.** Implementar a API REST simples (`GET /clientes`, `GET /clientes/{id}`) com **dados sintéticos** (ex.: Faker), com volumes configuráveis (10, 100, 1 000, 10 000 registos).
- [ ] **8.** Garantir que o backend só aceita ligações do middleware (rede interna, porta não exposta ou chave partilhada).

## Fase 3 – Núcleo do middleware *(Implementação – 8 valores)*

Seguir esta ordem, porque cada componente depende do anterior.

- [ ] **9.** **Autenticação e identificação do perfil:** validar assinatura e validade do token e extrair o perfil dele, nunca de um parâmetro do pedido. Devolver 401/403 sem contactar o backend.
- [ ] **10.** **Encaminhamento:** reenviar o pedido autorizado ao backend e receber a resposta completa.
- [ ] **11.** **Motor de políticas:** carregar a configuração, selecionar regras por (recurso, perfil), omitir por defeito os campos não previstos e aplicar *fail-closed* (se a política falhar, recusar a resposta).
- [ ] **12.** **Transformadores:**
  - [ ] manter
  - [ ] omitir
  - [ ] mascarar
  - [ ] generalizar
  - [ ] pseudonimizar (HMAC-SHA256, chave fora do código e da configuração)
  - [ ] agregar (respeitando o `k` mínimo)
- [ ] **13.** **Entrega da resposta:** erros e cabeçalhos que não revelam detalhes internos do backend.
- [ ] **14.** **Registo e métricas:** perfil, recurso, latência, `S_orig`, `S_trans` e ∆D, sem dados pessoais nos logs.

## Fase 4 – Componente adaptativo (Capítulo 4)

> Só avançar depois de as Fases 2, 3 e 5 estarem fechadas.

- [ ] **15.** Implementar o cálculo da entropia **H(X)** dos atributos antes e depois da transformação.
- [ ] **16.** Implementar uma função simples de risco **R(t)** (ex.: origem do pedido, horário, finalidade declarada) e a variante de política mais restritiva quando R(t) ultrapassa o limiar.
- [ ] **17.** Concretizar a utilidade **U ≥ U_min** (ex.: percentagem de campos úteis mantidos). Se não houver tempo, documentar como limitação.

## Fase 5 – Testes funcionais e de segurança *(Testes – parte dos 6 valores)*

- [ ] **18.** Escrever testes automáticos (`pytest`) que verifiquem que:
  - [ ] cada perfil recebe exatamente os campos e transformações previstos;
  - [ ] token ausente, inválido, expirado ou adulterado é rejeitado;
  - [ ] passar `?perfil=admin` ou um cabeçalho forjado não tem efeito;
  - [ ] campos novos no backend não são expostos;
  - [ ] uma falha na política resulta em recusa e não no payload original;
  - [ ] agregações abaixo de `k` não são divulgadas;
  - [ ] os logs não contêm dados pessoais;
  - [ ] o backend não é acessível diretamente.

## Fase 6 – Benchmarks e comparativos *(Testes – parte dos 6 valores)*

- [ ] **19.** Escrever os scripts de benchmark (Locust, `wrk`/`hey` ou script próprio com `httpx`/`asyncio`), com aquecimento e várias repetições.
- [ ] **20.** Comparar **acesso direto vs. através do middleware**, para cada perfil, variando o número de registos e a concorrência.
- [ ] **21.** Medir:
  - [ ] latência média, p50 e p95;
  - [ ] CPU e memória do processo do middleware (`psutil`);
  - [ ] `S_orig`, `S_trans` e ∆D por perfil;
  - [ ] H(X) antes e depois.
- [ ] **22.** Guardar os resultados em CSV, gerar tabelas e gráficos, e interpretar os números (custo do middleware vs. ganho em payload e exposição).

## Fase 7 – Validação do protótipo *(4 valores)*

- [ ] **23.** Cruzar o protótipo com os requisitos da Parte 1 (secção 2.3), numa checklist de *cumprido / parcial / não cumprido*:
  - [ ] autorização antes da transformação
  - [ ] políticas explícitas por perfil
  - [ ] proteção do fluxo e dos componentes
  - [ ] verificação funcional e de segurança
  - [ ] avaliação do impacto
- [ ] **24.** Rever as ameaças da secção 5.4 (ponto único de falha, *bypass* do backend, gestão de chaves) e registar o que foi testado.
- [ ] **25.** Discutir as limitações com honestidade: mascaragem e pseudonimização não equivalem a anonimização; as métricas não provam conformidade legal; existe custo de latência; R(t) e U foram simplificadas.
- [ ] **26.** Pedir a um elemento que não programou o módulo que reproduza tudo a partir do README.

## Fase 8 – Repositório e reprodutibilidade

- [ ] **27.** Finalizar o README (arquitetura, instalação, execução, testes, benchmarks), o `requirements.txt` ou `docker-compose`, e incluir resultados e documentação das políticas.

## Fase 9 – Relatório e vídeo *(2 valores)*

- [ ] **28.** Escrever o relatório da Parte 2 no mesmo template da Parte 1, com os capítulos de implementação, testes, resultados, validação e conclusões, com tabelas e figuras legíveis.
- [ ] **29.** Gravar o vídeo de apresentação:
  - [ ] arquitetura em 1 minuto;
  - [ ] demonstração dos três perfis com o mesmo pedido;
  - [ ] token inválido a ser rejeitado;
  - [ ] resultados do benchmark;
  - [ ] ensaio antes da gravação.

---

## Pontos de atenção

- Fechar o núcleo (Fases 2 e 3) e os testes (Fase 5) **antes** de investir na parte adaptativa (Fase 4). Um protótipo simples e bem testado pontua mais do que um ambicioso e incompleto.
- Implementação (8) e testes/comparativos (6) valem 70% da nota: reservar o tempo em proporção.