import pandas as pd
import plotly.graph_objects as go

from styles.theme import (
    ACCENT, ACCENT2, ACCENT3, ACCENT4, GRID_COLOR,
    TEXT_MAIN, TEXT_MUTED, LAYOUT_BASE, AXIS_STYLE,
)
from utils.formatters import format_currency

_BG_DARK = "#111114"

MESES_ORDER = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
               "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

CAT_COLORS = [ACCENT, ACCENT2, ACCENT4, "#4ECDC4", ACCENT3]

_LEGEND_TOP = dict(
    bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_MUTED, size=11),
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="left",
    x=0,
)


def _base(**overrides) -> dict:
    """Merge LAYOUT_BASE with per-chart overrides without keyword conflicts."""
    return {**LAYOUT_BASE, **overrides}


def get_revenue_by_month(df: pd.DataFrame) -> go.Figure:
    anos = sorted(df["ano"].unique())
    fig = go.Figure()
    palette = {anos[0]: ACCENT2, anos[-1]: ACCENT} if len(anos) > 1 else {anos[0]: ACCENT}

    for ano in anos:
        df_ano = (
            df[df["ano"] == ano]
            .groupby("mes_nome", sort=False)["receita"]
            .sum()
            .reindex(MESES_ORDER, fill_value=0)
            .reset_index()
        )
        df_ano.columns = ["mes", "receita"]
        is_latest = ano == max(anos)

        fig.add_trace(
            go.Scatter(
                x=df_ano["mes"],
                y=df_ano["receita"],
                name=str(ano),
                mode="lines+markers",
                line=dict(color=palette[ano], width=2.5, dash="solid" if is_latest else "dot"),
                marker=dict(size=6, color=palette[ano]),
                fill="tozeroy" if is_latest else "none",
                fillcolor="rgba(200,240,74,0.06)" if is_latest else "rgba(0,0,0,0)",
                hovertemplate="%{x}: <b>%{customdata}</b><extra></extra>",
                customdata=[format_currency(v) for v in df_ano["receita"]],
            )
        )

    fig.update_layout(
        **_base(
            title=dict(text="Receita Mensal", font=dict(size=14, color=TEXT_MAIN), x=0),
            xaxis=dict(**AXIS_STYLE, categoryorder="array", categoryarray=MESES_ORDER),
            yaxis=dict(**AXIS_STYLE, tickprefix="R$ ", tickformat=",.0f"),
            legend=_LEGEND_TOP,
            hovermode="x unified",
            margin=dict(l=0, r=0, t=36, b=0),
        )
    )
    return fig


def get_revenue_by_category(df: pd.DataFrame) -> go.Figure:
    df_cat = (
        df.groupby("categoria")["receita"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )
    df_cat.columns = ["categoria", "receita"]

    fig = go.Figure(
        go.Bar(
            x=df_cat["receita"],
            y=df_cat["categoria"],
            orientation="h",
            marker=dict(
                color=df_cat["receita"],
                colorscale=[[0, "#1e2e0a"], [1, ACCENT]],
                showscale=False,
            ),
            text=[format_currency(v) for v in df_cat["receita"]],
            textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=11),
            hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base(
            title=dict(text="Receita por Categoria", font=dict(size=14, color=TEXT_MAIN), x=0),
            xaxis=dict(**AXIS_STYLE, tickprefix="R$ ", tickformat=",.0f"),
            yaxis=dict(**AXIS_STYLE, showgrid=False),
            showlegend=False,
            margin=dict(l=0, r=90, t=36, b=0),
        )
    )
    return fig


def get_revenue_by_region(df: pd.DataFrame) -> go.Figure:
    df_reg = (
        df.groupby("regiao")["receita"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    df_reg.columns = ["regiao", "receita"]

    bar_colors = [ACCENT if i == 0 else ACCENT2 if i == 1 else "#3a3a4a"
                  for i in range(len(df_reg))]

    fig = go.Figure(
        go.Bar(
            x=df_reg["regiao"],
            y=df_reg["receita"],
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[format_currency(v) for v in df_reg["receita"]],
            textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=11),
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base(
            title=dict(text="Receita por Região", font=dict(size=14, color=TEXT_MAIN), x=0),
            xaxis=dict(**AXIS_STYLE, showgrid=False),
            yaxis=dict(**AXIS_STYLE, tickprefix="R$ ", tickformat=",.0f"),
            showlegend=False,
            margin=dict(l=0, r=0, t=36, b=0),
        )
    )
    return fig


def get_top_sellers(df: pd.DataFrame) -> go.Figure:
    df_vend = (
        df.groupby("vendedor")
        .agg(receita=("receita", "sum"), meta=("meta", "sum"))
        .assign(atingimento=lambda x: x["receita"] / x["meta"] * 100)
        .sort_values("receita", ascending=True)
        .reset_index()
    )

    bar_colors = [ACCENT if a >= 100 else ACCENT3 for a in df_vend["atingimento"]]
    hover_text = [
        f"<b>{v}</b><br>Receita: {format_currency(r)}<br>"
        f"Meta: {format_currency(m)}<br>Atingimento: {a:.1f}%"
        for v, r, m, a in zip(
            df_vend["vendedor"], df_vend["receita"],
            df_vend["meta"], df_vend["atingimento"],
        )
    ]

    fig = go.Figure(
        go.Bar(
            x=df_vend["receita"],
            y=df_vend["vendedor"],
            orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{a:.0f}%" for a in df_vend["atingimento"]],
            textposition="inside",
            textfont=dict(color=_BG_DARK, size=11),
            hovertext=hover_text,
            hoverinfo="text",
        )
    )
    fig.update_layout(
        **_base(
            title=dict(text="Top Vendedores", font=dict(size=14, color=TEXT_MAIN), x=0),
            xaxis=dict(**AXIS_STYLE, tickprefix="R$ ", tickformat=",.0f"),
            yaxis=dict(**AXIS_STYLE, showgrid=False),
            showlegend=False,
            margin=dict(l=0, r=0, t=36, b=0),
        )
    )
    return fig


def get_value_distribution(df: pd.DataFrame) -> go.Figure:
    categorias = sorted(df["categoria"].unique())
    fig = go.Figure()

    for i, cat in enumerate(categorias):
        cor = CAT_COLORS[i % len(CAT_COLORS)]
        r, g, b = _hex_to_rgb(cor)
        receitas = df[df["categoria"] == cat]["receita"]
        fig.add_trace(
            go.Box(
                y=receitas,
                name=cat,
                marker=dict(color=cor),
                line=dict(color=cor),
                fillcolor=f"rgba({r},{g},{b},0.15)",
                boxmean="sd",
                hovertemplate="<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>",
            )
        )

    fig.update_layout(
        **_base(
            title=dict(text="Distribuição por Categoria", font=dict(size=14, color=TEXT_MAIN), x=0),
            yaxis=dict(**AXIS_STYLE, tickprefix="R$ ", tickformat=",.0f"),
            xaxis=dict(**AXIS_STYLE, showgrid=False),
            showlegend=False,
            boxmode="group",
            margin=dict(l=0, r=0, t=36, b=0),
        )
    )
    return fig


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
