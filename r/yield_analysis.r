# yield_analysis.R
# 📊 Analysis of Dry Grain Yield using ANOVA, Regression, and DiD

# 🔧 Load required libraries
library(tidyverse)
library(broom)
library(lmtest)
library(sandwich)

# 📁 Import dataset
file_path <- "C:/Users/HP/Documents/Python For Data Science/data/raw data/yield_data.csv"
data <- read_csv(file_path)

# 📊 Visualize dry grain yield distribution
ggplot(data, aes(x = dry_grain_yield)) +
  geom_histogram(binwidth = 100, fill = "darkgreen", color = "black") +
  labs(title = "Distribution of Dry Grain Yield", x = "Dry Grain Yield", y = "Count")

# 🧹 Clean data: remove rows with missing values
data_clean <- data %>%
  drop_na(site, crop, treatment, replicate, dry_grain_yield)

# 📋 Summary statistics
summary(data_clean)
glimpse(data_clean)

# 🧪 ANOVA: Compare yield across treatments
anova_result <- aov(dry_grain_yield ~ treatment, data = data_clean)
summary(anova_result)

# 📈 Regression: Effects of treatment and crop on yield
regression_model <- lm(dry_grain_yield ~ treatment + crop, data = data_clean)
summary(regression_model)

# 🔄 Difference-in-Differences (DiD) Analysis
# Create proxy variables for before/after and treatment status
data_clean <- data_clean %>%
  mutate(
    BeforeAfter = if_else(replicate %in% c("R1", "R2", "R3"), 0, 1),
    TreatmentBinary = if_else(treatment %in% c("T1", "T2", "T3"), 1, 0),
    DiD = TreatmentBinary * BeforeAfter
  )

# Run DiD model
did_model <- lm(dry_grain_yield ~ TreatmentBinary + BeforeAfter + DiD, data = data_clean)
summary(did_model)
