import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")

df = pd.read_sql_query(
    "SELECT * FROM sales_transactions WHERE order_status='Completed'",
    sqlite3.connect("sales.db"),
    parse_dates=["order_date"]
)

fig = plt.figure(figsize=(14, 9))

plt.subplot(2, 3, 1)
sns.histplot(df["total_amount"], bins=10)
plt.title("Distribution of Order Value")

plt.subplot(2, 3, 2)
sns.histplot(df["quantity"], bins=10)
plt.title("Distribution of Quantity Ordered")

plt.subplot(2, 3, 3)
df.groupby("category")["total_amount"].sum().sort_values().plot(kind="barh")
plt.title("Revenue by Category")

plt.subplot(2, 3, 4)
monthly = df.groupby(df["order_date"].dt.to_period("M"))["total_amount"].sum()
monthly.plot()
plt.title("Monthly Revenue Trend")

plt.subplot(2, 3, 5)
sns.scatterplot(x="quantity", y="total_amount", data=df)
plt.title("Quantity vs Total Amount")

plt.subplot(2, 3, 6)
sns.heatmap(df[["quantity", "unit_price", "total_amount"]].corr(),
            annot=True, cmap="coolwarm")
plt.title("Correlation Between Numeric Variables")

plt.suptitle("Exploratory Data Analysis Dashboard", fontsize=12)
plt.tight_layout()
plt.savefig("outputs/EDA_Dashboard.png")
plt.show()

