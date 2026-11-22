"""Gerador de clientes sintéticos do Banco Exemplo (ver docs/recurso-clientes.md).

Os dados são reprodutíveis: a mesma semente gera sempre os mesmos clientes,
e os primeiros k clientes são iguais para qualquer volume n >= k.
"""

import random
import unicodedata
from datetime import date, timedelta

from faker import Faker

SEMENTE = 42

# Data de referência fixa para calcular idades (não depende do dia em que se corre).
DATA_REFERENCIA = date(2026, 1, 1)
IDADE_MIN, IDADE_MAX = 18, 90

DOMINIO_EMAIL = "exemplo.pt"

# distrito -> (peso aproximado pela população, {concelho: código postal base CP4})
GEOGRAFIA: dict[str, tuple[float, dict[str, int]]] = {
    "Aveiro": (7.0, {"Aveiro": 3800, "Águeda": 3750, "Ovar": 3880}),
    "Beja": (1.4, {"Beja": 7800, "Moura": 7860}),
    "Braga": (8.0, {"Braga": 4700, "Guimarães": 4800, "Barcelos": 4750}),
    "Bragança": (1.2, {"Bragança": 5300, "Mirandela": 5370}),
    "Castelo Branco": (1.7, {"Castelo Branco": 6000, "Covilhã": 6200}),
    "Coimbra": (4.0, {"Coimbra": 3000, "Figueira da Foz": 3080}),
    "Évora": (1.5, {"Évora": 7000, "Estremoz": 7100}),
    "Faro": (4.5, {"Faro": 8000, "Loulé": 8100, "Portimão": 8500}),
    "Guarda": (1.4, {"Guarda": 6300, "Seia": 6270}),
    "Leiria": (4.5, {"Leiria": 2400, "Caldas da Rainha": 2500}),
    "Lisboa": (22.0, {"Lisboa": 1000, "Sintra": 2710, "Cascais": 2750, "Loures": 2670}),
    "Portalegre": (1.0, {"Portalegre": 7300, "Elvas": 7350}),
    "Porto": (17.0, {"Porto": 4000, "Vila Nova de Gaia": 4400, "Matosinhos": 4450, "Maia": 4470}),
    "Santarém": (4.0, {"Santarém": 2000, "Tomar": 2300}),
    "Setúbal": (8.0, {"Setúbal": 2900, "Almada": 2800, "Seixal": 2840}),
    "Viana do Castelo": (2.3, {"Viana do Castelo": 4900, "Ponte de Lima": 4990}),
    "Vila Real": (2.0, {"Vila Real": 5000, "Chaves": 5400}),
    "Viseu": (3.5, {"Viseu": 3500, "Lamego": 5100}),
    "Região Autónoma dos Açores": (2.4, {"Ponta Delgada": 9500, "Angra do Heroísmo": 9700}),
    "Região Autónoma da Madeira": (2.5, {"Funchal": 9000, "Santa Cruz": 9100, "Câmara de Lobos": 9300}),
}

DISTRITOS = list(GEOGRAFIA)


def digito_controlo_nif(oito_digitos: str) -> int:
    """Dígito de controlo do NIF português (módulo 11, pesos 9..2)."""
    soma = sum(int(d) * peso for d, peso in zip(oito_digitos, range(9, 1, -1)))
    resto = 11 - soma % 11
    return 0 if resto >= 10 else resto


def _gerar_nif(rng: random.Random) -> str:
    # Pessoas singulares: começa por 1 ou 2.
    base = str(rng.choice((1, 2))) + "".join(str(rng.randint(0, 9)) for _ in range(7))
    return base + str(digito_controlo_nif(base))


def _sem_acentos(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", texto) if c.isascii() and c.isalnum())


def _gerar_data_nasc(rng: random.Random) -> date:
    mais_novo = DATA_REFERENCIA.replace(year=DATA_REFERENCIA.year - IDADE_MIN)
    mais_velho = DATA_REFERENCIA.replace(year=DATA_REFERENCIA.year - IDADE_MAX - 1) + timedelta(days=1)
    return mais_velho + timedelta(days=rng.randint(0, (mais_novo - mais_velho).days))


def gerar_clientes(n: int, semente: int = SEMENTE) -> list[dict]:
    """Gera n clientes sintéticos com o esquema de docs/recurso-clientes.md."""
    if n < 1:
        raise ValueError("n tem de ser >= 1")

    rng = random.Random(semente)
    fake = Faker("pt_PT")
    fake.seed_instance(semente)

    pesos = [GEOGRAFIA[d][0] for d in DISTRITOS]
    emails_usados: dict[str, int] = {}
    clientes = []

    for i in range(1, n + 1):
        nome_proprio, apelido = fake.first_name(), fake.last_name()

        local = f"{_sem_acentos(nome_proprio)}.{_sem_acentos(apelido)}".lower()
        emails_usados[local] = emails_usados.get(local, 0) + 1
        if emails_usados[local] > 1:
            local += str(emails_usados[local])

        distrito = rng.choices(DISTRITOS, weights=pesos)[0]
        concelho, cp4_base = rng.choice(list(GEOGRAFIA[distrito][1].items()))
        codigo_postal = f"{cp4_base + 10 * rng.randint(0, 9)}-{rng.randint(0, 999):03d}"

        clientes.append({
            "id": i,
            "nome": f"{nome_proprio} {apelido}",
            "email": f"{local}@{DOMINIO_EMAIL}",
            "nif": _gerar_nif(rng),
            "data_nasc": _gerar_data_nasc(rng).isoformat(),
            "morada": fake.street_address(),
            "codigo_postal": codigo_postal,
            "concelho": concelho,
            "distrito": distrito,
            # Log-normal: muitos saldos baixos, poucos altos (mediana ~1 100 EUR).
            "saldo": round(rng.lognormvariate(7.0, 1.2), 2),
        })

    return clientes
