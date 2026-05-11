def format_currency(value: float) -> str:
    return f"R$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value: float) -> str:
    return f"{value:.1f}%"


def format_number(value: float) -> str:
    return f"{int(value):,}".replace(",", ".")
