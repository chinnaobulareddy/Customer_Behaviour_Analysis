#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Basic cleaning for the already-loaded df
# - parse timestamps
# - standardize strings (strip/lower)
# - coerce numeric types
# - drop exact duplicate rows
# - add a few helpful derived columns
# - light missing-value handling (keep as NA, but normalize empty strings)

import pandas as pd

df_clean = df.copy()

# Parse event_time to timezone-aware datetime
if 'event_time' in df_clean.columns:
    df_clean['event_time'] = pd.to_datetime(df_clean['event_time'], errors='coerce', utc=True)

# Standardize common string columns
string_cols = [c for c in ['event_type', 'category_code', 'brand', 'user_session'] if c in df_clean.columns]
for col_name in string_cols:
    df_clean[col_name] = (
        df_clean[col_name]
        .astype('string')
        .str.strip()
        .replace({'': pd.NA, 'nan': pd.NA, 'None': pd.NA})
    )

# Lowercase selected categorical text fields
for col_name in [c for c in ['event_type', 'category_code', 'brand'] if c in df_clean.columns]:
    df_clean[col_name] = df_clean[col_name].str.lower()

# Coerce numeric columns
for col_name in [c for c in ['price', 'product_id', 'category_id', 'user_id'] if c in df_clean.columns]:
    df_clean[col_name] = pd.to_numeric(df_clean[col_name], errors='coerce')

# Drop exact duplicate rows
rows_before = len(df_clean)
df_clean = df_clean.drop_duplicates()
rows_after = len(df_clean)

# Derived time columns (useful for analysis)
if 'event_time' in df_clean.columns:
    df_clean['event_date'] = df_clean['event_time'].dt.date
    df_clean['event_hour'] = df_clean['event_time'].dt.hour

# Basic sanity filters (keep conservative)
# Price should not be negative
if 'price' in df_clean.columns:
    df_clean.loc[df_clean['price'] < 0, 'price'] = pd.NA

print(df_clean.head())
print(rows_before)
print(rows_after)

# Quick missingness snapshot for key columns
key_cols = [c for c in ['event_time','event_type','product_id','category_id','category_code','brand','price','user_id','user_session'] if c in df_clean.columns]
missing_rates = (df_clean[key_cols].isna().mean().sort_values(ascending=False) * 100).round(2)
print(missing_rates.head(10))

# Save cleaned file for download
out_path = '2020-Jan_cleaned.csv'
df_clean.to_csv(out_path, index=False)
print(out_path)

