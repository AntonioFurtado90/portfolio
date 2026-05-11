import pandas as pd
import streamlit as st

from utils.formatters import format_currency, format_number, format_percent


def render_kpis(df: pd.DataFrame, df_full: pd.DataFrame) -> None:
    receita_total = df["receita"].sum()
    ticket_medio = df["receita"].mean() if len(df) else 0
    total_pedidos = len(df)
    atingimento_meta = (df["receita"].sum() / df["meta"].sum() * 100) if df["meta"].sum() > 0 else 0

    # YoY delta: compare anos presentes no filtro
    anos = sorted(df["ano"].unique().tolist())
    delta_receita = delta_pedidos = delta_ticket = None
    if len(anos) >= 2:
        ano_atual = max(anos)
        ano_ant = ano_atual - 1
        if ano_ant in anos:
            rec_atual = df[df["ano"] == ano_atual]["receita"].sum()
            rec_ant = df[df["ano"] == ano_ant]["receita"].sum()
            ped_atual = len(df[df["ano"] == ano_atual])
            ped_ant = len(df[df["ano"] == ano_ant])
            tick_atual = df[df["ano"] == ano_atual]["receita"].mean()
            tick_ant = df[df["ano"] == ano_ant]["receita"].mean()

            if rec_ant:
                delta_receita = f"{(rec_atual - rec_ant) / rec_ant * 100:+.1f}% vs {ano_ant}"
            if ped_ant:
                delta_pedidos = f"{(ped_atual - ped_ant) / ped_ant * 100:+.1f}% vs {ano_ant}"
            if tick_ant:
                delta_ticket = f"{(tick_atual - tick_ant) / tick_ant * 100:+.1f}% vs {ano_ant}"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receita Total", format_currency(receita_total), delta=delta_receita)
    col2.metric("Ticket Médio", format_currency(ticket_medio), delta=delta_ticket)
    col3.metric("Total de Pedidos", format_number(total_pedidos), delta=delta_pedidos)
    col4.metric("Atingimento da Meta", format_percent(atingimento_meta))
