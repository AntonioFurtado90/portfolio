# Looker Studio — HR Analysis Report

**Public report:** _link after build_

---

## Data sources (4 tabs — add each separately in Looker Studio)

| Tab | Date field | Use |
|---|---|---|
| `funcionarios` | _(none)_ | Headcount snapshot, salary, absences, status |
| `dim_calendario` | `data_inicio_mes` | Calendar reference — year/month/quarter filters |
| `fato_admissoes` | **`data_admissao`** | All admission charts — one date column only |
| `fato_demissoes` | **`data_saida`** | All termination charts — one date column only |

> Looker Studio only supports one Date Range Dimension per data source.
> Keeping admissions and terminations in separate tabs solves this limitation.

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

### Page 2 — Admissões (source: `fato_admissoes`, Date Range Dimension: `data_admissao`)

| Chart | Type | Dimension | Metric |
|---|---|---|---|
| Admissões ao longo do tempo | Line chart | ano_mes | COUNT(id_funcionario) |
| Admissões por departamento/mês | Stacked bar | ano_mes + departamento | COUNT(id_funcionario) |
| Total admitido por departamento | Bar chart | departamento | COUNT(id_funcionario) |
| Admissões por trimestre | Bar chart | trimestre | COUNT(id_funcionario) |

### Page 3 — Demissões (source: `fato_demissoes`, Date Range Dimension: `data_saida`)

| Chart | Type | Dimension | Metric |
|---|---|---|---|
| Demissões ao longo do tempo | Line chart | ano_mes | COUNT(id_funcionario) |
| Demissões por departamento/mês | Stacked bar | ano_mes + departamento | COUNT(id_funcionario) |
| Turnover por departamento | Bar chart | departamento | COUNT(id_funcionario) |
| Demissões por trimestre | Bar chart | trimestre | COUNT(id_funcionario) |

### Page 4 — Headcount & Salários

| Chart | Type | Source | Dimension | Metric |
|---|---|---|---|---|
| Ativos vs Desligados | Donut chart | funcionarios | status | COUNT(id) |
| Headcount por departamento | Bar chart | funcionarios | departamento | COUNT(id) |
| Distribuição salarial | Histogram | funcionarios | salario | — |
| Salário médio por departamento | Bar chart | funcionarios | departamento | AVG(salario) |
| Faltas médias por departamento | Bar chart | funcionarios | departamento | AVG(media_faltas_mes) |

---

## Calculated fields (create in Looker Studio — source: `funcionarios`)

| Field name | Formula | Use |
|---|---|---|
| `Turnover %` | `COUNT(CASE WHEN status = "Desligado" THEN id_funcionario ELSE NULL END) / COUNT(id_funcionario)` | Turnover scorecard — format as % |
| `Total Ativos` | `COUNT(CASE WHEN status = "Ativo" THEN id_funcionario ELSE NULL END)` | Headcount ativo |
| `Total Desligados` | `COUNT(CASE WHEN status = "Desligado" THEN id_funcionario ELSE NULL END)` | Total de desligamentos |

> In Looker Studio: **Resource → Manage added data sources → Edit → Add a field**

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
