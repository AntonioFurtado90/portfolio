"""Generates synthetic sales dataset and saves to data/sales.csv."""

import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

VENDEDORES = [
    "Ana Silva", "Bruno Costa", "Carlos Lima", "Diana Santos",
    "Eduardo Rocha", "Fernanda Alves", "Gustavo Pereira", "Helena Martins",
]

CATEGORIAS = {
    "Eletrônicos":         dict(min=150,  max=3500, weight=0.20, meta_factor=1.25),
    "Roupas & Calçados":   dict(min=40,   max=500,  weight=0.25, meta_factor=1.10),
    "Casa & Jardim":       dict(min=30,   max=800,  weight=0.18, meta_factor=1.05),
    "Alimentos & Bebidas": dict(min=20,   max=250,  weight=0.22, meta_factor=0.95),
    "Esportes & Lazer":    dict(min=50,   max=1200, weight=0.15, meta_factor=1.15),
}

REGIOES = {
    "Sudeste":      dict(estados=["SP", "RJ", "MG", "ES"], weight=0.45, meta_factor=1.20),
    "Sul":          dict(estados=["RS", "PR", "SC"],       weight=0.20, meta_factor=1.10),
    "Nordeste":     dict(estados=["BA", "PE", "CE", "MA"], weight=0.18, meta_factor=1.00),
    "Centro-Oeste": dict(estados=["GO", "MT", "MS", "DF"], weight=0.10, meta_factor=0.95),
    "Norte":        dict(estados=["AM", "PA", "RO", "TO"], weight=0.07, meta_factor=0.88),
}

N_ROWS = 8_000
START = "2023-01-01"
END = "2024-12-31"


def _seasonal_weight(date: pd.Timestamp) -> float:
    m = date.month
    if m == 11:
        return 2.4   # Black Friday
    if m == 12:
        return 2.0   # Natal
    if m == 6:
        return 1.3   # Dia dos Namorados
    if m == 10:
        return 1.2   # Dia das Crianças
    if m in (1, 2):
        return 1.1   # Verão
    return 1.0


def generate() -> None:
    dates = pd.date_range(START, END, freq="D")
    weights = np.array([_seasonal_weight(d) for d in dates], dtype=float)
    weights /= weights.sum()

    sampled = np.random.choice(len(dates), size=N_ROWS, p=weights)
    sampled_dates = dates[sampled]

    cat_names = list(CATEGORIAS.keys())
    cat_w = np.array([CATEGORIAS[c]["weight"] for c in cat_names])
    cat_w = cat_w / cat_w.sum()

    reg_names = list(REGIOES.keys())
    reg_w = np.array([REGIOES[r]["weight"] for r in reg_names])
    reg_w = reg_w / reg_w.sum()

    rows = []
    for data in sampled_dates:
        cat = np.random.choice(cat_names, p=cat_w)
        regiao = np.random.choice(reg_names, p=reg_w)
        estado = np.random.choice(REGIOES[regiao]["estados"])
        vendedor = np.random.choice(VENDEDORES)

        cfg = CATEGORIAS[cat]
        receita = round(float(np.random.uniform(cfg["min"], cfg["max"])), 2)
        qtd_itens = int(np.random.randint(1, 7))

        # meta reflects difficulty: Eletrônicos+Sudeste é mais difícil de bater
        fator = cfg["meta_factor"] * REGIOES[regiao]["meta_factor"]
        noise = float(np.random.uniform(0.90, 1.10))
        meta = round(receita * fator * noise, 2)

        rows.append({
            "data": data.date(),
            "regiao": regiao,
            "estado": estado,
            "categoria": cat,
            "vendedor": vendedor,
            "receita": receita,
            "qtd_itens": qtd_itens,
            "meta": meta,
        })

    df = pd.DataFrame(rows).sort_values("data").reset_index(drop=True)
    out = Path(__file__).parent / "data" / "sales.csv"
    out.parent.mkdir(exist_ok=True)
    df.to_csv(out, index=False)
    print(f"✓ {len(df)} linhas geradas → {out}")


if __name__ == "__main__":
    generate()
