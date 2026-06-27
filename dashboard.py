# dashboard.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("online_retail.csv", encoding="latin1")
df = df.drop_duplicates()
df = df.dropna(subset=["CustomerID"])
df = df[(df["Quantity"]>0)&(df["UnitPrice"]>0)]
df["InvoiceDate"]=pd.to_datetime(df["InvoiceDate"])
df["Revenue"]=df["Quantity"]*df["UnitPrice"]
df["Month"]=df["InvoiceDate"].dt.to_period("M").astype(str)

total_revenue=df["Revenue"].sum()
total_orders=df["InvoiceNo"].nunique()
total_customers=df["CustomerID"].nunique()
avg_order=total_revenue/total_orders

monthly_revenue=df.groupby("Month")["Revenue"].sum()
monthly_orders=df.groupby("Month")["InvoiceNo"].nunique()
top_products=df.groupby("Description")["Revenue"].sum().nlargest(10)
top_countries=df.groupby("Country")["Revenue"].sum().nlargest(10)
top_customers=df.groupby("CustomerID")["Revenue"].sum().nlargest(10)
heat=df.pivot_table(values="Revenue",
                    index=df["InvoiceDate"].dt.year,
                    columns=df["InvoiceDate"].dt.month,
                    aggfunc="sum",fill_value=0)

plt.style.use("dark_background")
fig=plt.figure(figsize=(24,16),facecolor="#0B1020")
gs=GridSpec(4,4,figure=fig,height_ratios=[0.8,2,2,2])
fig.suptitle("Retail Sales Analytics Dashboard",fontsize=28,fontweight="bold")

cards=[
("Revenue",f"£{total_revenue:,.0f}","#1abc9c"),
("Orders",f"{total_orders:,}","#3498db"),
("Customers",f"{total_customers:,}","#9b59b6"),
("Avg Order",f"£{avg_order:.2f}","#e67e22")
]
for i,(t,v,c) in enumerate(cards):
    ax=fig.add_subplot(gs[0,i]); ax.set_facecolor(c)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.text(.5,.65,t,ha="center",fontsize=16,fontweight="bold")
    ax.text(.5,.25,v,ha="center",fontsize=20,fontweight="bold")

ax=fig.add_subplot(gs[1,0:2]); monthly_revenue.plot(ax=ax,marker="o",color="cyan")
ax.fill_between(range(len(monthly_revenue)),monthly_revenue.values,color="cyan",alpha=.25)
ax.set_title("Monthly Revenue")

ax=fig.add_subplot(gs[1,2:4]); monthly_orders.plot(ax=ax,marker="o",color="orange")
ax.fill_between(range(len(monthly_orders)),monthly_orders.values,color="orange",alpha=.25)
ax.set_title("Monthly Orders")

ax=fig.add_subplot(gs[2,0]); sns.barplot(x=top_products.values,y=top_products.index,ax=ax,palette="viridis")
ax.set_title("Top Products")

ax=fig.add_subplot(gs[2,1]); sns.barplot(x=top_countries.values,y=top_countries.index,ax=ax,palette="magma")
ax.set_title("Top Countries")

ax=fig.add_subplot(gs[2,2]); sns.barplot(x=top_customers.values,y=top_customers.index.astype(str),ax=ax,palette="crest")
ax.set_title("Top Customers")

ax=fig.add_subplot(gs[2,3])
ax.pie(top_countries.values,labels=top_countries.index,autopct="%1.1f%%",wedgeprops={"width":0.45})
ax.set_title("Country Revenue Share")

ax=fig.add_subplot(gs[3,0:2])
sns.heatmap(heat,cmap="YlOrRd",ax=ax)
ax.set_title("Revenue Heatmap")

ax=fig.add_subplot(gs[3,2:4]); ax.axis("off")
txt=f"""BUSINESS INSIGHTS

Revenue: £{total_revenue:,.0f}
Orders: {total_orders}
Customers: {total_customers}
Average Order: £{avg_order:.2f}

Top Country: {top_countries.index[0]}
Top Product:
{top_products.index[0]}

RECOMMENDATIONS
• Focus on best-selling products
• Retain top customers
• Increase inventory before peak months
• Expand outside dominant market
• Optimize low-selling products
"""
ax.text(0,1,txt,va="top",fontsize=14,
bbox=dict(boxstyle="round",facecolor="#1f2937",alpha=.9))

plt.tight_layout(rect=[0,0,1,.96])
plt.savefig("outputs/dashboard.png",dpi=300)
plt.show()
