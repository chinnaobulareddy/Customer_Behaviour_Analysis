#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Load the uploaded CSV and do a quick sanity check (head + basic shape)
import pandas as pd

csv_path = "2019-Dec.csv"
df = pd.read_csv(csv_path, encoding="ascii")

print(df.head())
print(df.shape)


# In[ ]:


# Data cleaning: standardize types, handle missing values, remove obvious invalid rows, and add useful time features
import pandas as pd
import numpy as np

# Work on a copy to keep the original raw df available
clean_df = df.copy()

# Parse datetime (force UTC) and drop rows with invalid timestamps
clean_df["event_time"] = pd.to_datetime(clean_df["event_time"], errors="coerce", utc=True)
clean_df = clean_df.dropna(subset=["event_time"]).copy()

# Standardize event_type
clean_df["event_type"] = clean_df["event_type"].astype("string").str.strip().str.lower()
valid_event_types = {"view", "cart", "remove_from_cart", "purchase"}
clean_df = clean_df[clean_df["event_type"].isin(valid_event_types)].copy()

# Numeric coercions
clean_df["price"] = pd.to_numeric(clean_df["price"], errors="coerce")
clean_df["product_id"] = pd.to_numeric(clean_df["product_id"], errors="coerce", downcast="integer")
clean_df["category_id"] = pd.to_numeric(clean_df["category_id"], errors="coerce")
clean_df["user_id"] = pd.to_numeric(clean_df["user_id"], errors="coerce", downcast="integer")

# Drop rows missing essential identifiers
clean_df = clean_df.dropna(subset=["product_id", "category_id", "user_id", "user_session"]).copy()

# Clean strings
clean_df["brand"] = clean_df["brand"].astype("string").str.strip().str.lower()
clean_df.loc[clean_df["brand"].isin(["", "nan", "none", "null"]), "brand"] = pd.NA

clean_df["category_code"] = clean_df["category_code"].astype("string").str.strip().str.lower()
clean_df.loc[clean_df["category_code"].isin(["", "nan", "none", "null"]), "category_code"] = pd.NA

clean_df["user_session"] = clean_df["user_session"].astype("string").str.strip()

# Remove invalid prices
# Assumption: price should be > 0 for all events; if price is missing/<=0, drop those rows
clean_df = clean_df[clean_df["price"].notna() & (clean_df["price"] > 0)].copy()

# Remove extreme outliers (winsorize by filtering) to avoid crazy values skewing analysis
# Assumption: keep within 0.1th to 99.9th percentile
p_low = clean_df["price"].quantile(0.001)
p_high = clean_df["price"].quantile(0.999)
clean_df = clean_df[(clean_df["price"] >= p_low) & (clean_df["price"] <= p_high)].copy()

# Add useful time features
clean_df["event_date"] = clean_df["event_time"].dt.date
clean_df["event_hour"] = clean_df["event_time"].dt.hour
clean_df["event_dow"] = clean_df["event_time"].dt.day_name()

# De-duplicate exact duplicate rows (rare but safe)
clean_df = clean_df.drop_duplicates()

# Show before/after and a quick head
print(df.shape)
print(clean_df.shape)
print(clean_df.head())

# Quick missingness after cleaning
missing_after = (clean_df.isna().mean().sort_values(ascending=False) * 100).round(2)
print(missing_after.head(10))


# In[ ]:


# Quick EDA: parse time, basic missingness, event mix, and a few key plots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Parse event_time to datetime (already looks timezone-aware in the preview)
df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce", utc=True)

# Basic summaries
row_count = len(df)
col_count = df.shape[1]
min_time = df["event_time"].min()
max_time = df["event_time"].max()

missing_rate = (df.isna().mean().sort_values(ascending=False) * 100).round(2)
event_counts = df["event_type"].value_counts(dropna=False)

print(row_count)
print(col_count)
print(min_time)
print(max_time)
print(missing_rate.head(10))
print(event_counts)

# Time series of events per day
by_day = df.groupby(df["event_time"].dt.date)["event_type"].size().reset_index(name="events")
by_day = by_day.sort_values("event_time")

plt.figure(figsize=(10,4))
sns.lineplot(data=by_day, x="event_time", y="events")
plt.title("Events per day (Dec 2019)")
plt.xlabel("day")
plt.ylabel("events")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Event type distribution
plt.figure(figsize=(6,4))
sns.barplot(x=event_counts.index, y=event_counts.values, color="#4C72B0")
plt.title("Event type counts")
plt.xlabel("event_type")
plt.ylabel("count")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()

# Price distribution (log scale) for non-null prices
price_vals = pd.to_numeric(df["price"], errors="coerce")
price_vals = price_vals[price_vals.notna() & (price_vals > 0)]

plt.figure(figsize=(8,4))
sns.histplot(np.log10(price_vals), bins=60, color="#55A868")
plt.title("Price distribution (log10)")
plt.xlabel("log10(price)")
plt.ylabel("count")
plt.tight_layout()
plt.show()

