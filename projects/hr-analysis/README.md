# HR Analysis — Looker Studio

People Analytics report built with Looker Studio, connected live to a Google Sheets datasource populated by a Python script.

**Live report:** _link after deploy_

---

## Dataset

150 synthetic employees (2022–2025) across 5 departments:
- **Comercial · Operações · TI · RH · Financeiro**
- Fields: id, name, department, role, hire date, termination date, status, salary, avg monthly absences
- ~18% annual turnover rate

## Key metrics & charts

- KPI scorecards: total headcount, turnover %, avg tenure, avg absences
- Headcount by department — bar chart
- Active vs terminated — donut chart
- Admissions over time — line chart (monthly)
- Turnover by department — bar chart
- Salary distribution — histogram
- Absences heatmap by department

## Stack

| Tool | Purpose |
|---|---|
| Looker Studio | Dashboard and visualization |
| Google Sheets | Live data source |
| Python + gspread | Data generation and push |
| Faker | Synthetic employee names |

## Running locally

```bash
cd projects/hr-analysis
pip install -r requirements.txt

# Configure credentials
cp .env.example .env
# Edit .env with your Google Sheet ID and credentials path

# Generate and push data
python generate_data.py
```

## Google Sheets setup

1. Create a Google Sheet and copy its ID from the URL
2. Share the sheet with your service account email (Editor access)
3. Add the Sheet ID to `.env`
4. Run `generate_data.py`

## Connecting to Looker Studio

1. Looker Studio → Create → Report → Google Sheets
2. Select the HR Analysis sheet
3. Build charts (see `looker_studio_link.md` for full chart list)
4. Share → Anyone with the link can view
