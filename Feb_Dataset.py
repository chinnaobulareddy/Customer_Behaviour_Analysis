#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Clean df_feb2020 in-place: standardize columns, parse datetimes, coerce numerics, drop duplicates,
# handle missing values, and remove obvious invalid rows. Then show a quick before/after summary.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Before snapshot ---
rows_before = len(df_feb2020)
dupes_before = int(df_feb2020.duplicated().sum())
na_before = df_feb2020.isna().sum().sort_values(ascending=False)

# --- Standardize column names ---
df_feb2020.columns = [str(col).strip().lower().replace(' ', '_') for col in df_feb2020.columns]

# --- Parse datetime columns if present ---
for dt_col in ['event_time', 'time', 'timestamp', 'datetime']:
    if dt_col in df_feb2020.columns:
        df_feb2020[dt_col] = pd.to_datetime(df_feb2020[dt_col], errors='coerce', utc=True)

# --- Coerce common numeric columns ---
for num_col in ['price', 'user_id', 'product_id', 'category_id', 'order_id']:
    if num_col in df_feb2020.columns:
        df_feb2020[num_col] = pd.to_numeric(df_feb2020[num_col], errors='coerce')

# --- Trim whitespace in object columns ---
obj_cols = df_feb2020.select_dtypes(include=['object']).columns
for col in obj_cols:
    df_feb2020[col] = df_feb2020[col].astype('string').str.strip()

# --- Drop exact duplicate rows ---
df_feb2020 = df_feb2020.drop_duplicates().reset_index(drop=True)

# --- Remove obviously invalid rows (common e-commerce clickstream assumptions) ---
# If event_type exists, drop rows where it's missing
if 'event_type' in df_feb2020.columns:
    df_feb2020 = df_feb2020[df_feb2020['event_type'].notna() & (df_feb2020['event_type'] != '')]

# If price exists, keep non-negative prices; allow NaN for non-purchase events
if 'price' in df_feb2020.columns:
    df_feb2020 = df_feb2020[(df_feb2020['price'].isna()) | (df_feb2020['price'] >= 0)]

# If user_id/product_id exist, drop rows missing them (usually required identifiers)
for id_col in ['user_id', 'product_id']:
    if id_col in df_feb2020.columns:
        df_feb2020 = df_feb2020[df_feb2020[id_col].notna()]

df_feb2020 = df_feb2020.reset_index(drop=True)

# --- After snapshot ---
rows_after = len(df_feb2020)
dupes_after = int(df_feb2020.duplicated().sum())
na_after = df_feb2020.isna().sum().sort_values(ascending=False)

print(df_feb2020.head())
print(rows_before)
print(rows_after)
print(dupes_before)
print(dupes_after)

# Show top missingness after cleaning
print(na_after.head(10))

# Quick visualization: missingness for top 10 columns with most NaNs
na_after_top = na_after.head(10)
plt.figure(figsize=(8,4))
plt.bar(na_after_top.index.astype(str), na_after_top.values)
plt.title('Top 10 columns by missing values (after cleaning)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# In[ ]:


# Load the CSV into df_feb2020 (it was not in memory due to the earlier cell not executing)
import pandas as pd

csv_path = './2020-Feb.csv'
df_feb2020 = pd.read_csv(csv_path)

print(df_feb2020.head())
print(len(df_feb2020))


# In[ ]:


# Clean df_feb2020: standardize columns, parse datetimes, coerce numerics, trim strings,
# drop duplicates, remove invalid rows, and save a cleaned CSV.
import pandas as pd
import numpy as np

rows_before = len(df_feb2020)
dupes_before = int(df_feb2020.duplicated().sum())

# Standardize column names
clean_cols = [str(col).strip().lower().replace(' ', '_') for col in df_feb2020.columns]
df_feb2020.columns = clean_cols

# Parse event_time
if 'event_time' in df_feb2020.columns:
    df_feb2020['event_time'] = pd.to_datetime(df_feb2020['event_time'], errors='coerce', utc=True)

# Coerce numeric columns
for num_col in ['product_id', 'category_id', 'price', 'user_id']:
    if num_col in df_feb2020.columns:
        df_feb2020[num_col] = pd.to_numeric(df_feb2020[num_col], errors='coerce')

# Trim whitespace for text columns
obj_cols = df_feb2020.select_dtypes(include=['object', 'string']).columns
for col in obj_cols:
    df_feb2020[col] = df_feb2020[col].astype('string').str.strip()

# Drop exact duplicates
df_feb2020 = df_feb2020.drop_duplicates().reset_index(drop=True)

# Remove invalid rows (practical assumptions for this dataset)
if 'event_type' in df_feb2020.columns:
    df_feb2020 = df_feb2020[df_feb2020['event_type'].notna() & (df_feb2020['event_type'] != '')]

if 'price' in df_feb2020.columns:
    df_feb2020 = df_feb2020[(df_feb2020['price'].isna()) | (df_feb2020['price'] >= 0)]

for id_col in ['user_id', 'product_id']:
    if id_col in df_feb2020.columns:
        df_feb2020 = df_feb2020[df_feb2020[id_col].notna()]

# Optional: normalize category_code/brand missing values to <NA>
for col in ['category_code', 'brand']:
    if col in df_feb2020.columns:
        df_feb2020[col] = df_feb2020[col].replace({'': pd.NA, 'none': pd.NA, 'None': pd.NA})

rows_after = len(df_feb2020)
dupes_after = int(df_feb2020.duplicated().sum())

# Save cleaned file
clean_path = './2020-Feb_cleaned.csv'
df_feb2020.to_csv(clean_path, index=False)

print(df_feb2020.head())
print(rows_before)
print(rows_after)
print(dupes_before)
print(dupes_after)
print(clean_path)

