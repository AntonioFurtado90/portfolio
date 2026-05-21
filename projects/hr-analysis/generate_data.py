"""
Generates synthetic HR dataset and pushes it to Google Sheets.
Idempotent: clears all tabs and rewrites on each run.

Tabs created:
  - funcionarios     : raw employee data (fact table)
  - dim_calendario   : calendar dimension linked to all dates in the period
  - admissoes_por_mes: headcount admitted per month/department
  - demissoes_por_mes: headcount terminated per month/department

Usage:
    pip install -r requirements.txt
    cp .env.example .env
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

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

N_FUNCIONARIOS = 150
DATA_INICIO = date(2022, 1, 1)
DATA_FIM = date(2025, 12, 31)
TAXA_TURNOVER_ANUAL = 0.18


# ── Fact table ────────────────────────────────────────────────────────────────

def generate_employees() -> pd.DataFrame:
    rows = []
    for i in range(1, N_FUNCIONARIOS + 1):
        depto = random.choice(list(DEPARTAMENTOS.keys()))
        cargo = random.choice(DEPARTAMENTOS[depto])

        dias_total = (DATA_FIM - DATA_INICIO).days
        data_admissao = DATA_INICIO + timedelta(days=random.randint(0, dias_total - 180))

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


# ── Calendar dimension ────────────────────────────────────────────────────────

def build_calendar() -> pd.DataFrame:
    """Monthly calendar dimension covering the full data period."""
    periods = pd.period_range(start=DATA_INICIO, end=DATA_FIM, freq="M")
    rows = []
    for p in periods:
        rows.append({
            "ano_mes":    str(p),                          # "2022-01"
            "ano":        p.year,
            "mes":        p.month,
            "mes_nome":   MESES_PT[p.month],
            "trimestre":  f"T{p.quarter}/{p.year}",
            "semestre":   f"S{'1' if p.month <= 6 else '2'}/{p.year}",
            "data_inicio_mes": p.start_time.date().strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)


# ── Aggregated views ──────────────────────────────────────────────────────────

def build_admissoes_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Admissions per month and department, joined with calendar keys."""
    admissoes = df.copy()
    admissoes["ano_mes"] = pd.to_datetime(admissoes["data_admissao"]).dt.to_period("M").astype(str)
    admissoes["ano"] = pd.to_datetime(admissoes["data_admissao"]).dt.year
    admissoes["mes"] = pd.to_datetime(admissoes["data_admissao"]).dt.month
    admissoes["mes_nome"] = admissoes["mes"].map(MESES_PT)
    admissoes["trimestre"] = pd.to_datetime(admissoes["data_admissao"]).dt.quarter.apply(lambda q: f"T{q}")

    agg = (
        admissoes.groupby(["ano_mes", "ano", "mes", "mes_nome", "trimestre", "departamento"])
        .size()
        .reset_index(name="total_admissoes")
        .sort_values(["ano_mes", "departamento"])
    )
    return agg


def build_demissoes_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Terminations per month and department, joined with calendar keys."""
    demissoes = df[df["data_saida"] != ""].copy()
    demissoes["ano_mes"] = pd.to_datetime(demissoes["data_saida"]).dt.to_period("M").astype(str)
    demissoes["ano"] = pd.to_datetime(demissoes["data_saida"]).dt.year
    demissoes["mes"] = pd.to_datetime(demissoes["data_saida"]).dt.month
    demissoes["mes_nome"] = demissoes["mes"].map(MESES_PT)
    demissoes["trimestre"] = pd.to_datetime(demissoes["data_saida"]).dt.quarter.apply(lambda q: f"T{q}")

    agg = (
        demissoes.groupby(["ano_mes", "ano", "mes", "mes_nome", "trimestre", "departamento"])
        .size()
        .reset_index(name="total_demissoes")
        .sort_values(["ano_mes", "departamento"])
    )
    return agg


# ── Google Sheets push ────────────────────────────────────────────────────────

def get_or_create_tab(spreadsheet, title: str):
    """Returns existing worksheet or creates a new one."""
    try:
        return spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows=500, cols=20)


def write_tab(ws, df: pd.DataFrame) -> None:
    ws.clear()
    data = [df.columns.tolist()] + df.astype(str).values.tolist()
    ws.update(range_name="A1", values=data)


def push_to_sheets(
    funcionarios: pd.DataFrame,
    calendario: pd.DataFrame,
    admissoes: pd.DataFrame,
    demissoes: pd.DataFrame,
) -> None:
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID não definido no .env")

    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(sheet_id)

    tabs = {
        "funcionarios":      funcionarios,
        "dim_calendario":    calendario,
        "admissoes_por_mes": admissoes,
        "demissoes_por_mes": demissoes,
    }

    for title, df in tabs.items():
        ws = get_or_create_tab(spreadsheet, title)
        write_tab(ws, df)
        print(f"  ✓ {title}: {len(df)} linhas")


# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Gerando dados...")
    funcionarios = generate_employees()
    calendario = build_calendar()
    admissoes = build_admissoes_por_mes(funcionarios)
    demissoes = build_demissoes_por_mes(funcionarios)

    print(f"  funcionarios:      {len(funcionarios)} registros")
    print(f"  dim_calendario:    {len(calendario)} meses")
    print(f"  admissoes_por_mes: {len(admissoes)} linhas")
    print(f"  demissoes_por_mes: {len(demissoes)} linhas")

    print("\nEnviando para o Google Sheets...")
    push_to_sheets(funcionarios, calendario, admissoes, demissoes)

    print(f"\n✓ Concluído!")
    print(f"  Ativos:     {len(funcionarios[funcionarios.status == 'Ativo'])}")
    print(f"  Desligados: {len(funcionarios[funcionarios.status == 'Desligado'])}")
