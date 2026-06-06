import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CREATE OUTPUT FOLDER

output_folder = "outputs"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("Output folder created successfully!")

# LOAD DATA

df = pd.read_csv("online_retail.csv", encoding="latin1")

print("Original Shape:", df.shape)

# DATA CLEANING

df.drop_duplicates(inplace=True)

df.dropna(subset=["CustomerID"], inplace=True)

df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("Cleaned Shape:", df.shape)

# KPI CALCULATIONS

total_revenue = df["Revenue"].sum()

total_orders = df["InvoiceNo"].nunique()

total_customers = df["CustomerID"].nunique()

avg_order_value = total_revenue / total_orders

# PRINT KPI

print("\n========== BUSINESS KPI ==========")

print(f"Total Revenue      : £{total_revenue:,.2f}")
print(f"Total Orders       : {total_orders}")
print(f"Total Customers    : {total_customers}")
print(f"Average Order Value: £{avg_order_value:.2f}")

# MONTHLY REVENUE TREND

df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
)

plt.figure(figsize=(12,6))

monthly_revenue.plot(marker='o')

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.grid(True)

plt.tight_layout()

plt.savefig("outputs/revenue_trend.png")

plt.close()

print("Revenue trend saved")

# TOP PRODUCTS

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

sns.barplot(
    x=top_products.values,
    y=top_products.index
)

plt.title("Top 10 Products By Revenue")
plt.xlabel("Revenue (£)")

plt.tight_layout()

plt.savefig("outputs/top_products.png")

plt.close()

print("Top products chart saved")

# TOP COUNTRIES

top_countries = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

sns.barplot(
    x=top_countries.values,
    y=top_countries.index
)

plt.title("Top 10 Countries By Revenue")
plt.xlabel("Revenue (£)")

plt.tight_layout()

plt.savefig("outputs/top_countries.png")

plt.close()

print("Top countries chart saved")

# TOP CUSTOMERS

top_customers = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

sns.barplot(
    x=top_customers.values,
    y=top_customers.index.astype(str)
)

plt.title("Top 10 Customers By Revenue")
plt.xlabel("Revenue (£)")

plt.tight_layout()

plt.savefig("outputs/top_customers.png")

plt.close()

print("Top customers chart saved")

# MONTHLY ORDERS

monthly_orders = (
    df.groupby("Month")["InvoiceNo"]
    .nunique()
)

plt.figure(figsize=(12,6))

monthly_orders.plot(marker='o')

plt.title("Monthly Orders Trend")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.grid(True)

plt.tight_layout()

plt.savefig("outputs/monthly_orders.png")

plt.close()

print("Monthly orders chart saved")

# REPORT GENERATION

report = f"""

RETAIL SALES ANALYSIS REPORT


Total Revenue: £{total_revenue:,.2f}

Total Orders: {total_orders}

Total Customers: {total_customers}

Average Order Value: £{avg_order_value:.2f}


TOP 5 PRODUCTS


{top_products.head().to_string()}


TOP 5 COUNTRIES


{top_countries.head().to_string()}


BUSINESS INSIGHTS


1. Focus marketing on top-selling products.

2. United Kingdom contributes majority revenue.

3. Retain top customers through loyalty programs.

4. Increase inventory before seasonal peaks.

5. Expand sales in high-performing countries.

6. Analyze low-performing products and optimize stock.
"""

with open("report.txt", "w") as f:
    f.write(report)

