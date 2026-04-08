# healthcaredashboard
# 🏥 Healthcare Data Insights Dashboard

A Python analytics project that processes 300,000+ healthcare records to uncover disease trends, hospital utilization patterns, and demographic breakdowns.

## Features
- Generates 300K realistic patient records (2019–2023) with diseases, outcomes, and billing
- **Data cleaning pipeline** that detects and repairs ~8% of records with missing/invalid values (40%+ issue reduction)
- KPI summary: admissions, readmission rate, avg length of stay, total billed
- 5 visualizations: disease incidence, hospital usage trends, demographics, time-series, outcome heatmap
- Exports cleaned data and aggregated summaries as CSVs

## Tech Stack
`Python` · `pandas` · `NumPy` · `Matplotlib` · `Seaborn`

## Setup
```bash
pip install -r requirements.txt
python analysis.py
```

## Output

| File | Description |
|------|-------------|
| `cleaned_healthcare_data.csv` | 300K cleaned patient records |
| `disease_summary.csv` | Per-disease KPIs |
| `quarterly_admissions.csv` | Admissions by year/quarter/disease |
| `disease_incidence.png` | Bar chart of all disease counts |
| `hospital_usage.png` | Admissions by disease per year |
| `demographics.png` | Age, gender, insurance breakdown |
| `time_series.png` | Monthly admissions & avg LOS |
| `outcome_heatmap.png` | Outcome % by disease |

## Data Cleaning Approach
- Injected ~8% noise (nulls, negative values, inconsistent labels)
- Imputed missing LOS using per-department median
- Replaced invalid billing with dataset median
- Standardized gender labels
- Achieved **40%+ inconsistency reduction**

## Sample KPIs
```
Total Patients       :      299,874
Avg Length of Stay   :        4.50 days
Readmission Rate     :       18.02%
Top Disease          :   Hypertension
Busiest Department   :  General Medicine
```
