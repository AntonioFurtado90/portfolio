# Looker Studio — HR Analysis Report

**Public report:** _link after build_

---

## Charts to build in Looker Studio

| Chart | Type | Dimension | Metric |
|---|---|---|---|
| Headcount total | Scorecard | — | COUNT(id_funcionario) WHERE status=Ativo |
| Turnover % | Scorecard | — | COUNT(Desligado) / COUNT(total) |
| Média de faltas/mês | Scorecard | — | AVG(media_faltas_mes) |
| Headcount por departamento | Bar chart | departamento | COUNT(id_funcionario) |
| Ativos vs Desligados | Donut chart | status | COUNT(id_funcionario) |
| Admissões ao longo do tempo | Line chart | data_admissao (mês) | COUNT(id_funcionario) |
| Turnover por departamento | Bar chart | departamento | COUNT WHERE status=Desligado |
| Distribuição salarial | Histogram | salario | — |
| Tempo médio de casa | Scorecard | — | AVG(data_saida - data_admissao) |

---

## Setup instructions

1. Go to [Looker Studio](https://lookerstudio.google.com)
2. **Create → Report → Add data → Google Sheets**
3. Select the HR Analysis sheet → connect
4. Build the charts above
5. **Share → Anyone with the link can view**
6. Copy the report URL and paste it here
