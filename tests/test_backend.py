"""Testes do backend de teste (tarefas 6 e 7)."""

import re
from datetime import date

import pytest
from fastapi.testclient import TestClient

from backend.app import CABECALHO_CHAVE, criar_app
from backend.dados import DATA_REFERENCIA, DISTRITOS, GEOGRAFIA, gerar_clientes

CHAVE = "chave-de-teste-" + "x" * 32
CAMPOS = {"id", "nome", "email", "nif", "data_nasc", "morada",
          "codigo_postal", "concelho", "distrito", "saldo"}


def cliente_http(n: int = 100) -> TestClient:
    return TestClient(criar_app(n=n, chave=CHAVE))


def nif_valido(nif: str) -> bool:
    """Verificação independente do dígito de controlo."""
    if not re.fullmatch(r"\d{9}", nif):
        return False
    soma = sum(int(nif[i]) * (9 - i) for i in range(8))
    controlo = 11 - soma % 11
    return int(nif[8]) == (0 if controlo >= 10 else controlo)


# --- Dados (tarefa 6) ---------------------------------------------------------

@pytest.mark.parametrize("n", [10, 100, 1000, 10000])
def test_volume(n):
    resposta = cliente_http(n).get("/clientes", headers={CABECALHO_CHAVE: CHAVE})
    assert resposta.status_code == 200
    assert len(resposta.json()) == n


def test_esquema_e_regras():
    clientes = gerar_clientes(1000)
    assert [c["id"] for c in clientes] == list(range(1, 1001))
    assert len({c["email"] for c in clientes}) == 1000, "emails repetidos"

    for c in clientes:
        assert set(c) == CAMPOS
        assert nif_valido(c["nif"]), c["nif"]
        assert c["email"].endswith("@exemplo.pt")
        assert c["distrito"] in DISTRITOS
        assert c["concelho"] in GEOGRAFIA[c["distrito"]][1], "concelho fora do distrito"
        assert re.fullmatch(r"\d{4}-\d{3}", c["codigo_postal"])
        assert c["saldo"] >= 0 and round(c["saldo"], 2) == c["saldo"]

        nasc = date.fromisoformat(c["data_nasc"])
        idade = DATA_REFERENCIA.year - nasc.year - (
            (DATA_REFERENCIA.month, DATA_REFERENCIA.day) < (nasc.month, nasc.day))
        assert 18 <= idade <= 90


def test_reprodutivel():
    assert gerar_clientes(100) == gerar_clientes(100)
    # Os primeiros registos não dependem do volume.
    assert gerar_clientes(1000)[:10] == gerar_clientes(10)


def test_obter_cliente():
    http = cliente_http()
    resposta = http.get("/clientes/7", headers={CABECALHO_CHAVE: CHAVE})
    assert resposta.status_code == 200
    assert resposta.json() == gerar_clientes(100)[6]

    assert http.get("/clientes/999", headers={CABECALHO_CHAVE: CHAVE}).status_code == 404


def test_sem_documentacao_exposta():
    http = cliente_http()
    for caminho in ("/docs", "/redoc", "/openapi.json"):
        assert http.get(caminho, headers={CABECALHO_CHAVE: CHAVE}).status_code == 404


@pytest.mark.parametrize("caminho, cabecalhos", [
    pytest.param("/clientes", {CABECALHO_CHAVE: CHAVE}, id="lista"),
    pytest.param("/clientes/1", {CABECALHO_CHAVE: CHAVE}, id="cliente"),
    pytest.param("/clientes/999", {CABECALHO_CHAVE: CHAVE}, id="nao_encontrado"),
    pytest.param("/clientes", {}, id="nao_autorizado"),
])
def test_json_declara_utf8(caminho, cabecalhos):
    """Sem charset, o PowerShell 5.1 mostra os acentos errados."""
    resposta = cliente_http().get(caminho, headers=cabecalhos)
    assert resposta.headers["content-type"] == "application/json; charset=utf-8"


# --- Acesso só pelo middleware (tarefa 7) ---------------------------------------

@pytest.mark.parametrize("cabecalhos", [
    pytest.param({}, id="sem_chave"),
    pytest.param({CABECALHO_CHAVE: "chave-errada"}, id="chave_errada"),
    pytest.param({CABECALHO_CHAVE: CHAVE[:-1]}, id="chave_quase_certa"),
])
@pytest.mark.parametrize("caminho", ["/clientes", "/clientes/1", "/inexistente"])
def test_rejeita_sem_chave_valida(cabecalhos, caminho):
    resposta = cliente_http().get(caminho, headers=cabecalhos)
    assert resposta.status_code == 401
    assert resposta.json() == {"erro": "Não autorizado"}


def test_nao_arranca_sem_chave(monkeypatch):
    monkeypatch.delenv("BACKEND_KEY", raising=False)
    with pytest.raises(RuntimeError):
        criar_app(n=10)
