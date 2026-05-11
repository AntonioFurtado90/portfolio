import pandas as pd
import streamlit as st


def render_sidebar(df: pd.DataFrame) -> dict:
    st.sidebar.title("Filtros")
    st.sidebar.markdown("---")

    anos = sorted(df["ano"].unique().tolist())
    anos_sel = st.sidebar.multiselect("Ano", anos, default=anos)

    categorias = sorted(df["categoria"].unique().tolist())
    cat_sel = st.sidebar.multiselect("Categoria", categorias, default=categorias)

    regioes = sorted(df["regiao"].unique().tolist())
    reg_sel = st.sidebar.multiselect("Região", regioes, default=regioes)

    vendedores = sorted(df["vendedor"].unique().tolist())
    vend_sel = st.sidebar.multiselect("Vendedor", vendedores, default=vendedores)

    return dict(anos=anos_sel, categorias=cat_sel, regioes=reg_sel, vendedores=vend_sel)


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    anos = filters["anos"] or df["ano"].unique().tolist()
    cats = filters["categorias"] or df["categoria"].unique().tolist()
    regs = filters["regioes"] or df["regiao"].unique().tolist()
    vends = filters["vendedores"] or df["vendedor"].unique().tolist()

    mask = (
        df["ano"].isin(anos)
        & df["categoria"].isin(cats)
        & df["regiao"].isin(regs)
        & df["vendedor"].isin(vends)
    )
    return df[mask].copy()
