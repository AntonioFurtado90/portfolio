import pandas as pd
import streamlit as st
from pathlib import Path

_DATA_PATH = Path(__file__).parent.parent / "data" / "sales.csv"

MESES_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}


@st.cache_data
def load_sales() -> pd.DataFrame:
    df = pd.read_csv(_DATA_PATH, parse_dates=["data"])
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["mes_nome"] = df["mes"].map(MESES_PT)
    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)
    return df
