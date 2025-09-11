# labor_force_analysis.py

# 📦 Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 📁 Load dataset
try:
    path = r"/Users/HP/Documents/Python For Data Science/data/raw data/Rw_Labor23.csv"
    tk = pd.read_csv(path, encoding='unicode_escape')
    print("✅ Dataset loaded successfully.")
    print(f"The dataset has {tk.shape[0]} rows and {tk.shape[1]} columns.")
except FileNotFoundError:
    print("❌ Error: Rw_Labor23.csv not found. Please make sure the CSV file is in the same directory as the script.")

# 🏷️ Rename columns for clarity
rename_map = {
    'A01': 'gender',
    'province': 'region',
    'weight2': 'weight',
    'status1': 'employment_status',
    'employed16': 'employed_flag',
    'PLF': 'in_labor_force',
    'LUU': 'unemployed_flag',
    'attained': 'education',
    'main_sect': 'sector',
    'isco2digit': 'occupation',
    'usualhrs': 'hours_usual',
    'acthrs': 'hours_actual',
    'act_hrs': 'hours_actual_alt',
    'cash': 'income_cash',
    'intcash': 'income_in_kind',
    'age10': 'age_group10',
    'age5': 'age_group5',
    'age3': 'age_group3',
}
tk.rename(columns=rename_map, inplace=True)

# 📊 Example analysis: Employment rate by gender
employment_rate = tk.groupby('gender')['employed_flag'].mean().round(2)
print("\n📊 Employment Rate by Gender:")
print(employment_rate)
