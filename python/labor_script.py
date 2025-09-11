# labor_script.py

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
###########################################################################################################################
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

###
# 1. Filter the data to include only those in the labor force.

# We look for people whose status is either 'Employed' or 'Unemployed'.

labor_force_df = tk[tk['employment_status'].isin(['Employed', 'Unemployed'])].copy()

# 2. Calculate the employment rate for each gender.
# pd.crosstab is a great tool for this. It creates a frequency table.
# normalize='index' calculates the percentages across each row (i.e., for each gender).
employment_rates = pd.crosstab(index=labor_force_df['gender'],
                               columns=labor_force_df['employment_status'],
                               normalize='index') * 100

# We only need the 'Employed' column for our plot.
rates_to_plot = employment_rates[['Employed']].reset_index()

# 3. Create the bar plot using Seaborn for a clean look.
plt.figure(figsize=(8, 6))
barplot = sns.barplot(x='gender', y='Employed', data=rates_to_plot, palette='viridis')

# This loop adds the percentage label on top of each bar for clarity.
for index, row in rates_to_plot.iterrows():
    barplot.text(index, row.Employed + 1, f"{row.Employed:.1f}%", color='black', ha="center", fontsize=12)

# 4. Add titles and labels to make the plot easy to understand.
plt.title('Employment Rate by Gender', fontsize=16)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Employment Rate (%)', fontsize=12)
plt.ylim(0, 110) # Give some space for the text above the bars.
plt.tight_layout()

# Save the plot to a file in your current directory.
plt.savefig('employment_rate_by_gender.png')

# Display the plot in your notebook.
plt.show()

# Print the final numbers in a clean table.
print("\nCalculated Employment Rates (%):")
print(rates_to_plot.to_markdown(index=False))

# We continue to use the 'tk' DataFrame from your previous steps.

# 1. Filter for the labor force (employed or unemployed individuals).
labor_force_df = tk[tk['employment_status'].isin(['Employed', 'Unemployed'])].copy()

# 2. Calculate the unemployment rate by region.
# We'll use crosstab again to get the counts of 'Employed' and 'Unemployed' in each region.
regional_status = pd.crosstab(index=labor_force_df['region'],
                              columns=labor_force_df['employment_status'])

# Calculate the unemployment rate: (Unemployed / (Unemployed + Employed)) * 100
regional_status['unemployment_rate'] = \
    (regional_status['Unemployed'] / (regional_status['Unemployed'] + regional_status['Employed'])) * 100

# Sort the results to make the chart easier to read.
rates_to_plot = regional_status[['unemployment_rate']].sort_values(by='unemployment_rate', ascending=False).reset_index()

# 3. Create the bar plot.
plt.figure(figsize=(12, 7))
barplot = sns.barplot(x='unemployment_rate', y='region', data=rates_to_plot, palette='plasma')

# 4. Add titles and labels for clarity.
plt.title('Unemployment Rate by Region', fontsize=16)
plt.xlabel('Unemployment Rate (%)', fontsize=12)
plt.ylabel('Region', fontsize=12)
plt.tight_layout()

# Save the plot to a file.
plt.savefig('unemployment_rate_by_region.png')

# Display the plot.
plt.show()

# Print the final numbers in a clean table.
print("\nCalculated Unemployment Rates (%):")
print(rates_to_plot.to_markdown(index=False))

# We continue to use the 'tk' DataFrame.

# 1. Prepare the income column.
# First, ensure the income column is numeric, turning non-numbers into missing values (NaN).
tk['income_cash'] = pd.to_numeric(tk['income_cash'], errors='coerce')

# For simplicity, we will define 'income' as 'income_cash'.
# We also drop rows with missing income to ensure the average is accurate.
income_df = tk[['education', 'income_cash']].dropna(subset=['income_cash'])

# 2. Calculate the average income by education level.
# We group by the 'education' column and calculate the mean of 'income_cash' for each group.
avg_income = income_df.groupby('education')['income_cash'].mean().sort_values(ascending=False).reset_index()

# 3. Create the bar plot.
plt.figure(figsize=(12, 8))
barplot = sns.barplot(x='income_cash', y='education', data=avg_income, palette='magma')

# 4. Add titles and labels for clarity.
plt.title('Average Monthly Income by Education Level', fontsize=16)
plt.xlabel('Average Income (RWF)', fontsize=12)
plt.ylabel('Education Level', fontsize=12)
plt.tight_layout()

# Save the plot to a file.
plt.savefig('average_income_by_education.png')

# Display the plot.
plt.show()

# Print the final numbers in a clean table.
print("\nCalculated Average Income by Education Level (RWF):")
print(avg_income.to_markdown(index=False))

# We continue to use the 'tk' DataFrame.

# 1. Prepare the age group column.
# We will use 'age_group10' as our primary age group column.
# Let's drop rows where the age group or employment status is missing.
age_df = tk[['age_group10', 'employment_status']].dropna()

# 2. Define who is in the labor force.
age_df['in_labor_force'] = age_df['employment_status'].isin(['Employed', 'Unemployed'])

# 3. Calculate the Labor Force Participation Rate (LFPR) by age group.
# We group by age group and find the percentage of people 'in_labor_force'.
lfpr = age_df.groupby('age_group10')['in_labor_force'].mean() * 100

# Convert to a DataFrame and sort it logically.
lfpr_df = lfpr.reset_index()

# Ensure a logical sort order for the plot (this handles cases like '65+' coming before '7-14')
# We extract the first number from the age group string to create a sorting key.
lfpr_df['sort_key'] = lfpr_df['age_group10'].str.extract('(\d+)').astype(int)
lfpr_df = lfpr_df.sort_values('sort_key').drop(columns='sort_key')


# 4. Create the line plot.
plt.figure(figsize=(12, 7))
sns.lineplot(x='age_group10', y='in_labor_force', data=lfpr_df, marker='o', sort=False)

# 5. Add titles and labels.
plt.title('Labor Force Participation Rate by Age Group', fontsize=16)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Participation Rate (%)', fontsize=12)
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()

# Save and show the plot.
plt.savefig('lfpr_by_age_group.png')
plt.show()

# Print the final numbers.
print("\nCalculated Labor Force Participation Rate (%):")
print(lfpr_df.to_markdown(index=False))

# We continue to use the 'tk' DataFrame.

# 1. Filter the DataFrame to include only employed people.
employed_df = tk[tk['employment_status'] == 'Employed'].copy()

# 2. Count the number of people in each sector.
# The value_counts() method is perfect for this.
sector_counts = employed_df['sector'].value_counts().reset_index()
sector_counts.columns = ['sector', 'count']

# 3. Create the horizontal bar plot.
plt.figure(figsize=(12, 8))
sns.barplot(x='count', y='sector', data=sector_counts, palette='crest')

# 4. Add titles and labels for clarity.
plt.title('Employment by Economic Sector', fontsize=16)
plt.xlabel('Number of People Employed', fontsize=12)
plt.ylabel('Sector', fontsize=12)
plt.tight_layout()

# Save and show the plot.
plt.savefig('employment_by_sector.png')
plt.show()

# Print the final counts in a table.
print("\nEmployment Counts by Sector:")
print(sector_counts.to_markdown(index=False))


##ETC....... I'd like you to please continue. 
