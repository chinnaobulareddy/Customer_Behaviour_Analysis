#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Basic cleaning for df_nov2019: parse time, standardize strings, coerce numerics, drop obvious bad rows, add helpful time columns
import pandas as pd

# Work on a copy so the original stays available if needed
nov_clean = df_nov2019.copy()

# Parse event_time (handles the trailing ' UTC')
nov_clean["event_time"] = pd.to_datetime(nov_clean["event_time"], errors="coerce", utc=True)

# Standardize string columns: strip whitespace, lowercase, and convert empty strings to NA
str_cols = ["event_type", "category_code", "brand", "user_session"]
for col_name in str_cols:
    if col_name in nov_clean.columns:
        nov_clean[col_name] = (
            nov_clean[col_name]
            .astype("string")
            .str.strip()
            .str.lower()
            .replace({"": pd.NA, "none": pd.NA, "nan": pd.NA})
        )

# Coerce numeric columns
nov_clean["price"] = pd.to_numeric(nov_clean["price"], errors="coerce")
for col_name in ["product_id", "category_id", "user_id"]:
    if col_name in nov_clean.columns:
        nov_clean[col_name] = pd.to_numeric(nov_clean[col_name], errors="coerce", downcast="integer")

# Remove obviously invalid rows
# - missing event_time/event_type/user_id/session
# - negative prices
nov_clean = nov_clean.dropna(subset=["event_time", "event_type", "user_id", "user_session"])
nov_clean = nov_clean[nov_clean["price"].isna() | (nov_clean["price"] >= 0)]

# Optional: remove exact duplicate rows
nov_clean = nov_clean.drop_duplicates()

# Add convenient time features
nov_clean["event_date"] = nov_clean["event_time"].dt.date
nov_clean["event_hour"] = nov_clean["event_time"].dt.hour

# Quick sanity checks
print(nov_clean.head())
print(nov_clean.shape)
print(nov_clean.isna().mean().sort_values(ascending=False).head(10))

