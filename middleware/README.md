# middleware

Núcleo do middleware de privacidade:

- autenticação e identificação do perfil (a partir do token);
- encaminhamento para o backend;
- motor de políticas (*fail-closed*, omissão por defeito);
- transformadores (manter, omitir, mascarar, generalizar, pseudonimizar, agregar);
- entrega da resposta;
- registo e métricas;
- componente adaptativo (H(X), R(t), U).
