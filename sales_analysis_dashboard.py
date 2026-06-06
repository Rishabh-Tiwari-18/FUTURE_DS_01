import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Create Output Folder

os.makedirs("outputs", exist_ok=True)


# Load Data

df = pd.read_csv("online_retail.csv", encoding="latin1")


# Data Cleaning

df.drop_duplicates(inplace=True)

df = df.dropna(subset=["CustomerID"])

df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Revenue"] = df["Quantity"] * df["UnitPrice"]


# KPI Metrics

total_revenue = df["Revenue"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
avg_order_value = total_revenue / total_orders


# Monthly Revenue

df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

monthly_revenue = df.groupby("Month")["Revenue"].sum()

monthly_orders = df.groupby("Month")["InvoiceNo"].nunique()


# Top Products

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


# Top Countries

top_countries = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


# Top Customers

top_customers = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


# Dashboard Layout

plt.style.use("default")

fig = plt.figure(figsize=(20, 14))

fig.suptitle(
    "Retail Sales Analytics Dashboard",
    fontsize=24,
    fontweight="bold"
)


# KPI CARDS


fig.text(
    0.05,
    0.90,
    f"Total Revenue\n£{total_revenue:,.0f}",
    fontsize=18,
    bbox=dict(boxstyle="round", pad=1)
)

fig.text(
    0.30,
    0.90,
    f"Total Orders\n{total_orders:,}",
    fontsize=18,
    bbox=dict(boxstyle="round", pad=1)
)

fig.text(
    0.55,
    0.90,
    f"Customers\n{total_customers:,}",
    fontsize=18,
    bbox=dict(boxstyle="round", pad=1)
)

fig.text(
    0.80,
    0.90,
    f"Avg Order Value\n£{avg_order_value:.2f}",
    fontsize=18,
    bbox=dict(boxstyle="round", pad=1)
)


# Revenue Trend

ax1 = plt.subplot(321)

monthly_revenue.plot(
    ax=ax1,
    marker="o"
)

ax1.set_title("Monthly Revenue Trend")
ax1.set_xlabel("")
ax1.set_ylabel("Revenue (£)")


# Monthly Orders

ax2 = plt.subplot(322)

monthly_orders.plot(
    ax=ax2,
    marker="o"
)

ax2.set_title("Monthly Orders Trend")
ax2.set_xlabel("")
ax2.set_ylabel("Orders")


# Top Products

ax3 = plt.subplot(323)

sns.barplot(
    x=top_products.values,
    y=top_products.index,
    ax=ax3
)

ax3.set_title("Top Products by Revenue")
ax3.set_xlabel("Revenue (£)")
ax3.set_ylabel("")


# Top Countries

ax4 = plt.subplot(324)

sns.barplot(
    x=top_countries.values,
    y=top_countries.index,
    ax=ax4
)

ax4.set_title("Top Countries by Revenue")
ax4.set_xlabel("Revenue (£)")
ax4.set_ylabel("")


# Top Customers

ax5 = plt.subplot(325)

sns.barplot(
    x=top_customers.values,
    y=top_customers.index.astype(str),
    ax=ax5
)

ax5.set_title("Top Customers by Revenue")
ax5.set_xlabel("Revenue (£)")
ax5.set_ylabel("Customer ID")


# Business Insights

ax6 = plt.subplot(326)

ax6.axis("off")

insights = f"""
KEY INSIGHTS

• Revenue: £{total_revenue:,.0f}

• UK is the dominant market

• Top products drive major revenue

• Customer concentration exists

• Seasonal sales patterns visible

RECOMMENDATIONS

1. Focus on top-selling products

2. Retain high-value customers

3. Expand in top countries

4. Optimize inventory for peak months

5. Improve low-performing products
"""

ax6.text(
    0,
    1,
    insights,
    fontsize=12,
    verticalalignment="top"
)

plt.tight_layout(rect=[0, 0, 1, 0.88])

plt.savefig(
    "outputs/dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

