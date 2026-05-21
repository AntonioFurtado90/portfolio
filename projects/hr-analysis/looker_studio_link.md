# Looker Studio — HR Analysis Report

**Public report:** _link after build_

---

## Data sources (4 tabs — add each separately in Looker Studio)

| Tab | Use |
|---|---|
| `funcionarios` | Main fact table — headcount, salary, absences |
| `dim_calendario` | Calendar dimension — join via `ano_mes` |
| `admissoes_por_mes` | Monthly admissions aggregated by department |
| `demissoes_por_mes` | Monthly terminations aggregated by department |

---

## How to connect

1. Looker Studio → **Create → Report → Add data → Google Sheets**
2. Select the HR Analysis spreadsheet
3. Select tab `funcionarios` → connect
4. Repeat for each additional tab (Add data → Google Sheets → same sheet, different tab)

---

## Charts to build

### Page 1 — Overview (KPI scorecards)

| Chart | Type | Source | Dimension | Metric |
|---|---|---|---|---|
| Total headcount ativo | Scorecard | funcionarios | — | COUNT(id) filter status=Ativo |
| Turnover % | Scorecard | funcionarios | — | COUNT(Desligado) / COUNT(total) |
| Média faltas/mês | Scorecard | funcionarios | — | AVG(media_faltas_mes) |
| Ticket médio salário | Scorecard | funcionarios | — | AVG(salario) |

### Page 2 — Admissões (linked to dim_calendario via ano_mes)

| Chart | Type | Source | Dimension | Metric |
|---|---|---|---|---|
| Admissões ao longo do tempo | Line chart | admissoes_por_mes | ano_mes | SUM(total_admissoes) |
| Admissões por departamento/mês | Stacked bar | admissoes_por_mes | ano_mes + departamento | SUM(total_admissoes) |
| Total admitido por departamento | Bar chart | admissoes_por_mes | departamento | SUM(total_admissoes) |
| Admissões por trimestre | Bar chart | admissoes_por_mes | trimestre | SUM(total_admissoes) |

### Page 3 — Demissões (linked to dim_calendario via ano_mes)

| Chart | Type | Source | Dimension | Metric |
|---|---|---|---|---|
| Demissões ao longo do tempo | Line chart | demissoes_por_mes | ano_mes | SUM(total_demissoes) |
| Demissões por departamento/mês | Stacked bar | demissoes_por_mes | ano_mes + departamento | SUM(total_demissoes) |
| Turnover por departamento | Bar chart | demissoes_por_mes | departamento | SUM(total_demissoes) |
| Demissões por trimestre | Bar chart | demissoes_por_mes | trimestre | SUM(total_demissoes) |

### Page 4 — Headcount & Salários

| Chart | Type | Source | Dimension | Metric |
|---|---|---|---|---|
| Ativos vs Desligados | Donut chart | funcionarios | status | COUNT(id) |
| Headcount por departamento | Bar chart | funcionarios | departamento | COUNT(id) |
| Distribuição salarial | Histogram | funcionarios | salario | — |
| Salário médio por departamento | Bar chart | funcionarios | departamento | AVG(salario) |
| Faltas médias por departamento | Bar chart | funcionarios | departamento | AVG(media_faltas_mes) |

---

## Calendar dimension usage

The `dim_calendario` tab provides clean time keys for all charts:
- `ano_mes` — primary join key (e.g. "2023-06")
- `ano` — year filter
- `trimestre` — quarter filter (e.g. "T1/2023")
- `semestre` — semester filter
- `mes_nome` — month label in Portuguese

Add a **date range control** using `ano_mes` from `dim_calendario` to filter all pages simultaneously.

---

## Sharing

After building the report:
1. Click **Share → Manage access**
2. Set to **Anyone with the link can view**
3. Copy the report URL and update this file
