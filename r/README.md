# 📊 R Scripts for Agronomy Analysis

This folder contains R scripts used to analyze dry grain yield data from field trials. The analysis includes:

- Data cleaning and visualization
- ANOVA to compare treatments
- Regression modeling of crop and treatment effects
- Difference-in-Differences (DiD) analysis to simulate impact over time

## 🧪 Script: `yield_analysis.R`

### Purpose
To explore how different treatments and crops affect dry grain yield, and simulate before/after effects using replicates as a proxy.

### How to Run
1. Open RStudio
2. Ensure required packages are installed:
   ```r
   install.packages(c("tidyverse", "broom", "lmtest", "sandwich")
