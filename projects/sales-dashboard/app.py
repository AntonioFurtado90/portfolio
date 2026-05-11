import streamlit as st

from components.charts import (
    get_revenue_by_category,
    get_revenue_by_month,
    get_revenue_by_region,
    get_top_sellers,
    get_value_distribution,
)
from components.filters import apply_filters, render_sidebar
from components.kpis import render_kpis
from styles.theme import ACCENT, BG_CARD, GRID_COLOR, TEXT_MUTED
from utils.data_loader import load_sales

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
        [data-testid="stMetric"] {{
            background: {BG_CARD};
            border: 1px solid {GRID_COLOR};
            border-radius: 10px;
            padding: 16px 20px;
        }}
        [data-testid="stMetricLabel"] {{ color: {TEXT_MUTED} !important; font-size: 0.82rem; }}
        [data-testid="stMetricValue"] {{ font-size: 1.6rem; font-weight: 700; }}
        [data-testid="stMetricDelta"] {{ font-size: 0.8rem; }}
        hr {{ border-color: {GRID_COLOR}; }}
        .block-container {{ padding-top: 2rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def main() -> None:
    df_full = load_sales()

    filters = render_sidebar(df_full)
    df = apply_filters(df_full, filters)

    st.title("Dashboard de Vendas")
    st.caption("Análise interativa de vendas 2023–2024 · Atualizado automaticamente ao ajustar os filtros")
    st.markdown("---")

    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    render_kpis(df, df_full)

    st.markdown("<br>", unsafe_allow_html=True)

    st.plotly_chart(get_revenue_by_month(df), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(get_revenue_by_category(df), use_container_width=True)
    with col_right:
        st.plotly_chart(get_revenue_by_region(df), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left2, col_right2 = st.columns(2)
    with col_left2:
        st.plotly_chart(get_top_sellers(df), use_container_width=True)
    with col_right2:
        st.plotly_chart(get_value_distribution(df), use_container_width=True)


if __name__ == "__main__":
    main()
