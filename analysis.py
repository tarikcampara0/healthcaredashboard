import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_healthcare_data(n=300_000):
    print(f"  Generating {n:,} records...")
    start = datetime(2019, 1, 1)
    end   = datetime(2023, 12, 31)
    delta = (end - start).days

    diseases   = ["Hypertension", "Diabetes", "Asthma", "COVID-19", "Depression",
                  "Heart Disease", "Obesity", "Cancer", "Arthritis", "Anxiety"]
    departments = ["Cardiology", "Oncology", "Pulmonology", "Psychiatry",
                   "General Medicine", "Orthopedics", "Endocrinology"]
    outcomes   = ["Recovered", "Recovered", "Recovered", "Admitted", "Admitted", "Referred", "Deceased"]
    insurance  = ["Medicare", "Medicaid", "Private", "Uninsured", "VA"]
    states     = ["CA", "TX", "NY", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]

    rows = []
    for i in range(n):
        dob_days  = random.randint(18 * 365, 85 * 365)
        age       = dob_days // 365
        disease   = random.choice(diseases)
        los       = max(1, int(np.random.exponential(4.5)))  # length of stay

        rows.append({
            "patient_id":    f"P{str(i).zfill(7)}",
            "date":          start + timedelta(days=random.randint(0, delta)),
            "age":           age,
            "gender":        random.choice(["Male", "Female", "Other"]),
            "state":         random.choice(states),
            "disease":       disease,
            "department":    random.choice(departments),
            "los_days":      los,"readmission":   random.choices([0, 1], weights=[0.82, 0.18])[0],
            "insurance":     random.choice(insurance),
            "outcome":       random.choice(outcomes),
            "billed_amount": round(los * random.uniform(1_200, 4_500), 2),
        })

    df = pd.DataFrame(rows)
    df["year"]      = df["date"].dt.year
    df["month"]     = df["date"].dt.month
    df["quarter"]   = df["date"].dt.quarter
    df["age_group"] = pd.cut(df["age"], bins=[0, 17, 34, 49, 64, 200],
                             labels=["0–17", "18–34", "35–49", "50–64", "65+"])
    return df
#kpi summary 
def print_kpis(df):
    total_patients   = df["patient_id"].nunique()
    avg_los          = df["los_days"].mean()
    readmit_rate     = df["readmission"].mean() * 100
    total_revenue    = df["billed_amount"].sum()
    top_disease      = df["disease"].value_counts().idxmax()
    most_used_dept   = df["department"].value_counts().idxmax()

    print("\n" + "=" * 55)
    print("         HEALTHCARE KPI DASHBOARD")
    print("=" * 55)
    print(f"  Total Patients       : {total_patients:>12,}")
    print(f"  Avg Length of Stay   : {avg_los:>11.2f} days")
    print(f"  Readmission Rate     : {readmit_rate:>11.2f}%")
    print(f"  Total Billed         : ${total_revenue:>12,.0f}")
    print(f"  Top Disease          : {top_disease:>15}")
    print(f"  Busiest Department   : {most_used_dept:>15}")
    print("=" * 55)
def plot_disease_incidence(df):
    counts = df["disease"].value_counts()

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(counts.index, counts.values,
                  color=[C["teal"] if i % 2 == 0 else C["slate"] for i in range(len(counts))])
    ax.set_title("Disease Incidence (All Records)", fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Disease"); ax.set_ylabel("Patient Count")
    ax.tick_params(axis="x", rotation=30)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f"{bar.get_height():,.0f}", ha="center", fontsize=8, color="#333")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/disease_incidence.png", dpi=150)
    plt.close()
    print(f"  Saved: disease_incidence.png")
def plot_hospital_usage(df):
    usage = df.groupby(["year", "disease"])["patient_id"].count().reset_index()
    pivot = usage.pivot(index="year", columns="disease", values="patient_id")

    fig, ax = plt.subplots(figsize=(14, 6))
    pivot.T.plot(kind="bar", ax=ax, colormap="tab10", width=0.8)
    ax.set_title("Hospital Usage by Disease per Year", fontsize=14, fontweight="bold")
    ax.set_xlabel("Disease"); ax.set_ylabel("Admissions")
    ax.tick_params(axis="x", rotation=40)
    ax.legend(title="Year", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/hospital_usage.png", dpi=150)
    plt.close()
    print(f"  Saved: hospital_usage.png")


def plot_demographic_breakdown(df):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
# age group
    age_counts = df["age_group"].value_counts().sort_index()
    axes[0].bar(age_counts.index.astype(str), age_counts.values, color=C["teal"])
    axes[0].set_title("Patients by Age Group", fontweight="bold")
    axes[0].set_ylabel("Count"); axes[0].grid(axis="y", alpha=0.3)

    # aender
    gen_counts = df["gender"].value_counts()
    axes[1].pie(gen_counts, labels=gen_counts.index, autopct="%1.1f%%",
                colors=[C["teal"], C["coral"], C["amber"]],
                wedgeprops={"edgecolor": "white", "linewidth": 2})
    axes[1].set_title("Gender Distribution", fontweight="bold")

    # insurance
    ins_counts = df["insurance"].value_counts()
    axes[2].barh(ins_counts.index, ins_counts.values, color=C["slate"])
    axes[2].set_title("Insurance Type", fontweight="bold")
    axes[2].set_xlabel("Count"); axes[2].grid(axis="x", alpha=0.3)

    fig.suptitle("Patient Demographics", fontsize=16, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/demographics.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: demographics.png")

def plot_time_series(df):
    monthly = df.groupby(["year", "month"]).agg(
        admissions=("patient_id", "count"),
        avg_los=("los_days", "mean"),
        readmissions=("readmission", "sum"),
    ).reset_index()
    monthly["date"] = pd.to_datetime(monthly[["year", "month"]].assign(day=1))
    monthly = monthly.sort_values("date")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    ax1.fill_between(monthly["date"], monthly["admissions"],
                     alpha=0.3, color=C["teal"])
    ax1.plot(monthly["date"], monthly["admissions"], color=C["teal"], linewidth=2)
    ax1.set_ylabel("Monthly Admissions"); ax1.grid(alpha=0.3)
    ax1.set_title("Monthly Admissions & Avg Length of Stay", fontsize=14, fontweight="bold")

    ax2.plot(monthly["date"], monthly["avg_los"], color=C["coral"], linewidth=2, marker="o", markersize=3)
    ax2.set_ylabel("Avg LOS (days)"); ax2.set_xlabel("Date"); ax2.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/time_series.png", dpi=150)
    plt.close()
    print(f"  Saved: time_series.png")

def plot_outcome_heatmap(df):
    pivot = df.pivot_table(values="patient_id", index="disease",
                           columns="outcome", aggfunc="count", fill_value=0)
    # Normalize to percentages
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(12, 7))
    sns.heatmap(pivot_pct, annot=True, fmt=".1f", cmap="RdYlGn",
                linewidths=0.5, ax=ax, cbar_kws={"label": "% of Disease Cases"})
    ax.set_title("Outcome Distribution by Disease (%)", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/outcome_heatmap.png", dpi=150)
    plt.close()
    print(f"  Saved: outcome_heatmap.png")
    
def export_data(df):
    df.to_csv(f"{OUTPUT_DIR}/cleaned_healthcare_data.csv", index=False)

    # Summary tables
    df.groupby("disease").agg(
        patients=("patient_id", "count"),
        avg_los=("los_days", "mean"),
        readmit_rate=("readmission", "mean"),
        avg_bill=("billed_amount", "mean"),
    ).reset_index().to_csv(f"{OUTPUT_DIR}/disease_summary.csv", index=False)

    df.groupby(["year", "quarter", "disease"])["patient_id"].count().reset_index(
        name="admissions"
    ).to_csv(f"{OUTPUT_DIR}/quarterly_admissions.csv", index=False)

    print(f"  Exported cleaned data and summaries to {OUTPUT_DIR}/")




