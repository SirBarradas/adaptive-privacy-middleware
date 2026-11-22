"""Backend de teste: sistema central de clientes do Banco Exemplo.

Só deve ser contactado pelo middleware (tarefa 7):
- escuta apenas em 127.0.0.1 (porta não exposta);
- exige o cabeçalho X-Backend-Key com a chave partilhada BACKEND_KEY.

Executar a partir da raiz do repositório:
    python -m backend.app
"""

import hmac
import json
import os

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from backend.dados import gerar_clientes

CABECALHO_CHAVE = "X-Backend-Key"
N_POR_DEFEITO = 100
TIPO_JSON = "application/json; charset=utf-8"


class JSONUtf8(JSONResponse):
    """JSON com charset explícito: sem ele, alguns clientes (ex.: Windows PowerShell 5.1)
    assumem ISO-8859-1 e mostram os acentos errados (Inês -> InÃªs)."""

    media_type = TIPO_JSON


def criar_app(n: int | None = None, chave: str | None = None) -> FastAPI:
    """Cria a aplicação. Sem argumentos, lê BACKEND_N_REGISTOS e BACKEND_KEY do ambiente."""
    n = n if n is not None else int(os.environ.get("BACKEND_N_REGISTOS", N_POR_DEFEITO))
    chave = chave if chave is not None else os.environ.get("BACKEND_KEY", "")
    if not chave:
        # Fail-closed: sem chave configurada, o backend não arranca.
        raise RuntimeError("BACKEND_KEY não definida (ver .env.example).")
    chave_bytes = chave.encode()

    # Dados gerados uma vez no arranque; a lista completa é serializada uma só vez,
    # para que os benchmarks meçam o middleware e não o backend.
    clientes = gerar_clientes(n)
    por_id = {c["id"]: c for c in clientes}
    lista_json = json.dumps(clientes, ensure_ascii=False).encode()

    app = FastAPI(
        title="Backend de teste – Banco Exemplo",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        default_response_class=JSONUtf8,
    )

    @app.middleware("http")
    async def exigir_chave(request: Request, call_next):
        recebida = request.headers.get(CABECALHO_CHAVE, "").encode()
        if not hmac.compare_digest(recebida, chave_bytes):
            return JSONUtf8({"erro": "Não autorizado"}, status_code=401)
        return await call_next(request)

    @app.get("/clientes")
    def listar_clientes():
        return Response(content=lista_json, media_type=TIPO_JSON)

    @app.get("/clientes/{cliente_id}")
    def obter_cliente(cliente_id: int):
        cliente = por_id.get(cliente_id)
        if cliente is None:
            return JSONUtf8({"erro": "Não encontrado"}, status_code=404)
        return cliente

    return app


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()
    uvicorn.run(
        criar_app(),
        host=os.environ.get("BACKEND_HOST", "127.0.0.1"),
        port=int(os.environ.get("BACKEND_PORT", 8001)),
        server_header=False,
    )
