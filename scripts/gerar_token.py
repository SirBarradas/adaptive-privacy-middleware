"""Gera tokens JWT de teste para os utilizadores definidos em docs/utilizadores-tokens.md.

Simula o fornecedor de identidade: o middleware só valida os tokens, não os emite.

Uso:
    python scripts/gerar_token.py analista
    python scripts/gerar_token.py publico --minutos 5

O segredo é lido da variável de ambiente JWT_SECRET (ou do ficheiro .env na raiz).
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from dotenv import load_dotenv

ISSUER = "apm-idp-teste"
AUDIENCE = "adaptive-privacy-middleware"
ALGORITMO = "HS256"

# perfil -> sub do utilizador de teste
UTILIZADORES = {
    "administrador": "admin01",
    "analista": "analista01",
    "publico": "publico01",
}


def gerar_token(perfil: str, segredo: str, minutos: int = 60) -> str:
    agora = datetime.now(timezone.utc)
    claims = {
        "iss": ISSUER,
        "aud": AUDIENCE,
        "sub": UTILIZADORES[perfil],
        "perfil": perfil,
        "iat": agora,
        "exp": agora + timedelta(minutes=minutos),
    }
    return jwt.encode(claims, segredo, algorithm=ALGORITMO)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera um token JWT de teste.")
    parser.add_argument("perfil", choices=UTILIZADORES)
    parser.add_argument("--minutos", type=int, default=60, help="validade (por defeito 60)")
    args = parser.parse_args()

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    segredo = os.environ.get("JWT_SECRET")
    if not segredo:
        sys.exit("Erro: defina JWT_SECRET (ver .env.example).")

    print(gerar_token(args.perfil, segredo, args.minutos))


if __name__ == "__main__":
    main()
