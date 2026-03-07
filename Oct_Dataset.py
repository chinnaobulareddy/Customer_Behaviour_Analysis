#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Load the uploaded CSV, do a quick sanity check, and keep df in memory
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_path = "2019-Oct.csv"
df = pd.read_csv(csv_path, encoding="ascii")

print(df.head())
print(df.shape)
print(df.isna().mean().sort_values(ascending=False).head(10))

# Quick look at event_type distribution
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="event_type", order=df["event_type"].value_counts().index)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# In[ ]:


# Clean the ecommerce clickstream dataset and export a GitHub-ready cleaned file
import pandas as pd

# Work off the already-loaded df
clean_df = df.copy()

# 1) Standardize column names
clean_df.columns = [c.strip().lower() for c in clean_df.columns]

# 2) Parse timestamps and add useful time features
clean_df["event_time"] = pd.to_datetime(clean_df["event_time"], utc=True, errors="coerce")
clean_df = clean_df.dropna(subset=["event_time", "event_type", "product_id", "category_id", "price", "user_id"])

clean_df["event_date"] = clean_df["event_time"].dt.date
clean_df["event_hour"] = clean_df["event_time"].dt.hour
clean_df["event_dow"] = clean_df["event_time"].dt.day_name()

# 3) Fix dtypes
clean_df["product_id"] = pd.to_numeric(clean_df["product_id"], errors="coerce").astype("Int64")
clean_df["category_id"] = pd.to_numeric(clean_df["category_id"], errors="coerce").astype("Int64")
clean_df["user_id"] = pd.to_numeric(clean_df["user_id"], errors="coerce").astype("Int64")
clean_df["price"] = pd.to_numeric(clean_df["price"], errors="coerce")

# 4) Clean strings
for col_name in ["category_code", "brand", "user_session", "event_type"]:
    if col_name in clean_df.columns:
        clean_df[col_name] = clean_df[col_name].astype("string").str.strip().str.lower()

# 5) Basic validity filters
clean_df = clean_df[clean_df["price"].notna()]
clean_df = clean_df[clean_df["price"] >= 0]
clean_df = clean_df[clean_df["event_type"].isin(["view", "cart", "purchase"])]

# 6) Handle missingness
# category_code is ~98% missing, keep it but fill with unknown for easier grouping
if "category_code" in clean_df.columns:
    clean_df["category_code"] = clean_df["category_code"].fillna("unknown")
# brand is ~40% missing, fill unknown
if "brand" in clean_df.columns:
    clean_df["brand"] = clean_df["brand"].fillna("unknown")

# 7) Remove exact duplicate rows
clean_df = clean_df.drop_duplicates()

# 8) Save cleaned dataset for GitHub
out_path = "2019-Oct_cleaned.csv"
clean_df.to_csv(out_path, index=False)

print(clean_df.head())
print(clean_df.shape)
print(out_path)

