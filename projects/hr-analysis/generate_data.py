"""
Generates synthetic HR dataset and pushes it to Google Sheets.
Idempotent: clears the sheet and rewrites all rows on each run.

Usage:
    pip install -r requirements.txt
    cp .env.example .env   # fill in credentials path and sheet ID
    python generate_data.py
"""

import os
import random
from datetime import date, timedelta

import gspread
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from faker import Faker
from google.oauth2.service_account import Credentials

load_dotenv()

fake = Faker("pt_BR")
np.random.seed(42)
random.seed(42)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

DEPARTAMENTOS = {
    "Comercial":   ["Vendedor Jr", "Vendedor Sr", "Coordenador de Vendas", "Gerente Comercial"],
    "Operações":   ["Analista de Operações", "Supervisor de Operações", "Coordenador"],
    "TI":          ["Desenvolvedor Jr", "Desenvolvedor Sr", "Analista de Dados", "DevOps"],
    "RH":          ["Analista de RH", "Recrutador", "HRBP", "Gerente de RH"],
    "Financeiro":  ["Assistente Financeiro", "Analista Financeiro", "Controller"],
}

FAIXAS_SALARIAIS = {
    "Comercial":   (2500, 9000),
    "Operações":   (2800, 7500),
    "TI":          (4000, 14000),
    "RH":          (2800, 8000),
    "Financeiro":  (3000, 10000),
}

N_FUNCIONARIOS = 150
DATA_INICIO = date(2022, 1, 1)
DATA_FIM = date(2025, 12, 31)
TAXA_TURNOVER_ANUAL = 0.18


def generate_employees() -> pd.DataFrame:
    rows = []
    for i in range(1, N_FUNCIONARIOS + 1):
        depto = random.choice(list(DEPARTAMENTOS.keys()))
        cargo = random.choice(DEPARTAMENTOS[depto])

        # Data de admissão distribuída ao longo do período
        dias_total = (DATA_FIM - DATA_INICIO).days
        data_admissao = DATA_INICIO + timedelta(days=random.randint(0, dias_total - 180))

        # Define se foi desligado (probabilidade proporcional ao tempo na empresa)
        meses_empresa = (date.today() - data_admissao).days / 30
        prob_desligamento = min(0.70, meses_empresa / 12 * TAXA_TURNOVER_ANUAL)
        desligado = random.random() < prob_desligamento

        if desligado:
            dias_permanencia = random.randint(60, (date.today() - data_admissao).days)
            data_saida = data_admissao + timedelta(days=dias_permanencia)
            status = "Desligado"
        else:
            data_saida = None
            status = "Ativo"

        sal_min, sal_max = FAIXAS_SALARIAIS[depto]
        salario = round(random.uniform(sal_min, sal_max), 2)

        # Faltas mensais: Poisson com média 0.8
        media_faltas = round(float(np.random.poisson(0.8)), 1)

        rows.append({
            "id_funcionario":   f"F{i:04d}",
            "nome":             fake.name(),
            "departamento":     depto,
            "cargo":            cargo,
            "data_admissao":    data_admissao.strftime("%Y-%m-%d"),
            "data_saida":       data_saida.strftime("%Y-%m-%d") if data_saida else "",
            "status":           status,
            "salario":          salario,
            "media_faltas_mes": media_faltas,
        })

    return pd.DataFrame(rows)


def push_to_sheets(df: pd.DataFrame) -> None:
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID não definido no .env")

    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1

    # Limpa e reescreve (idempotente)
    sheet.clear()
    headers = df.columns.tolist()
    data = [headers] + df.values.tolist()
    sheet.update(range_name="A1", values=data)

    print(f"✓ {len(df)} funcionários exportados para o Google Sheets")
    print(f"  Ativos:     {len(df[df.status == 'Ativo'])}")
    print(f"  Desligados: {len(df[df.status == 'Desligado'])}")


if __name__ == "__main__":
    print("Gerando dados...")
    funcionarios = generate_employees()
    print(f"✓ {len(funcionarios)} registros gerados")
    push_to_sheets(funcionarios)
