import sqlite3
import pandas as pd

print("Starting DB creation...")

data = [
    (1, 101, 1, "Widget A", "Gadgets", "2025-01-10", "Completed", 2, 50, 100, "India", "UPI"),
    (2, 102, 2, "Widget B", "Gadgets", "2025-02-15", "Completed", 1, 70, 70, "USA", "Card"),
]

columns = [
    "id", "customer_id", "product_id", "product_name", "category",
    "order_date", "order_status", "quantity", "unit_price",
    "total_amount", "country", "payment_method"
]

df = pd.DataFrame(data, columns=columns)

conn = sqlite3.connect("sales.db")
df.to_sql("sales_transactions", conn, if_exists="replace", index=False)
conn.close()

print("sales_transactions table CREATED")
