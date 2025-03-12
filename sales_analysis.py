import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Connect to SQLite Database
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Step 2: Load Walmart CSV File into Pandas
df = pd.read_csv("Walmart.csv")  # Ensure the file is in the correct location
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')  # Convert Date column correctly

# Step 3: Create SQLite Table & Insert Data
cursor.execute("DROP TABLE IF EXISTS Sales;")

cursor.execute('''
    CREATE TABLE Sales (
        Store INTEGER,
        Date TEXT,
        Weekly_Sales REAL,
        Holiday_Flag INTEGER,
        Temperature REAL,
        Fuel_Price REAL,
        CPI REAL,
        Unemployment REAL
    );
''')

df.to_sql("Sales", conn, if_exists="append", index=False)
print("Data inserted successfully!")

# Step 4: Perform SQL Queries
# Total Sales per Store
query = "SELECT Store, SUM(Weekly_Sales) AS TotalSales FROM Sales GROUP BY Store;"
df_sales = pd.read_sql(query, conn)
print(df_sales)

# Sales Trend Over Time
query = "SELECT Date, SUM(Weekly_Sales) AS DailySales FROM Sales GROUP BY Date ORDER BY Date;"
df_trend = pd.read_sql(query, conn)
print(df_trend)

# Step 5: Export Data to Excel
with pd.ExcelWriter("sales_report.xlsx", engine="openpyxl") as writer:
    df_sales.to_excel(writer, sheet_name="Total Sales Per Store", index=False)
    df_trend.to_excel(writer, sheet_name="Sales Trend", index=False)

print("Excel report generated successfully!")

# Step 6: Visualizations
# Bar Chart for Sales per Store
plt.figure(figsize=(8,5))
sns.barplot(x=df_sales['Store'], y=df_sales['TotalSales'], palette="viridis")
plt.title("Total Sales Per Store")
plt.xlabel("Store")
plt.ylabel("Total Sales")
plt.show()

# Line Chart for Sales Trend
plt.figure(figsize=(10,5))
plt.plot(df_trend["Date"], df_trend["DailySales"], marker='o', linestyle='-')
plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.show()

# Step 7: Close Database Connection
conn.close()
print("Database connection closed.")
