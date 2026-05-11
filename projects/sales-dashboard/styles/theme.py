ACCENT = "#C8F04A"
ACCENT2 = "#7B61FF"
ACCENT3 = "#FF6B6B"
ACCENT4 = "#FFB84C"
BG_MAIN = "#0D0D0F"
BG_CARD = "#16161A"
GRID_COLOR = "#1E1E24"
TEXT_MAIN = "#E8E6E0"
TEXT_MUTED = "#6B6B7A"

FONT = "Inter, system-ui, sans-serif"

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT, color=TEXT_MAIN, size=12),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_MUTED, size=11),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
    ),
)

AXIS_STYLE = dict(
    gridcolor=GRID_COLOR,
    linecolor=GRID_COLOR,
    zerolinecolor=GRID_COLOR,
    tickfont=dict(color=TEXT_MUTED, size=11),
    title_font=dict(color=TEXT_MUTED, size=12),
)
