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
