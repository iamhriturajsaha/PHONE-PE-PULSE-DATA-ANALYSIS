# Step 1 - Install necessary libraries
!pip install -q pandas matplotlib seaborn streamlit pyngrok plotly

# Step 2 - Clone the GitHub repository
!rm -rf pulse
!git clone https://github.com/PhonePe/pulse.git

# Step 3 - Create Database & Load Data
import os, json, sqlite3

# Connect to DB
conn = sqlite3.connect("phonepe.db")
cursor = conn.cursor()

# Create tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS aggregated_transaction (
    state TEXT, year INTEGER, quarter INTEGER,
    transaction_type TEXT, count INTEGER, amount REAL
);

CREATE TABLE IF NOT EXISTS aggregated_user_summary (
    state TEXT, year INTEGER, quarter INTEGER,
    registered_users INTEGER, app_opens INTEGER
);

CREATE TABLE IF NOT EXISTS aggregated_user_by_device (
    state TEXT, year INTEGER, quarter INTEGER,
    brand TEXT, user_count INTEGER, percentage REAL
);
""")

# Transaction Data
def extract_transaction_data():
    base_path = "pulse/data/aggregated/transaction/country/india"
    for year in os.listdir(base_path):
        for file in os.listdir(f"{base_path}/{year}"):
            if file.endswith(".json"):
                quarter = int(file.replace(".json", ""))
                with open(f"{base_path}/{year}/{file}") as f:
                    js = json.load(f)
                    for tx in js['data'].get('transactionData', []):
                        for pi in tx['paymentInstruments']:
                            cursor.execute("""
                                INSERT INTO aggregated_transaction VALUES (?, ?, ?, ?, ?, ?)
                            """, ("India", int(year), quarter, tx['name'], pi['count'], pi['amount']))
    conn.commit()

# User Data
def extract_user_data():
    base_path = "pulse/data/aggregated/user/country/india"
    for year in os.listdir(base_path):
        for file in os.listdir(f"{base_path}/{year}"):
            if file.endswith(".json"):
                quarter = int(file.replace(".json", ""))
                with open(f"{base_path}/{year}/{file}") as f:
                    js = json.load(f).get("data", {})
                    summary = js.get("aggregated", {})
                    cursor.execute("""
                        INSERT INTO aggregated_user_summary VALUES (?, ?, ?, ?, ?)
                    """, (
                        "India", int(year), quarter,
                        summary.get("registeredUsers", 0),
                        summary.get("appOpens", 0)
                    ))
                    users_by_device = js.get("usersByDevice", [])
                    if isinstance(users_by_device, list):
                        for dev in users_by_device:
                            cursor.execute("""
                                INSERT INTO aggregated_user_by_device VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                "India", int(year), quarter,
                                dev.get("brand", "Unknown"),
                                dev.get("count", 0),
                                dev.get("percentage", 0)
                            ))
    conn.commit()

# Load data
extract_transaction_data()
extract_user_data()
conn.close()
print("✅ Database created and populated.")

# Step 4 - Generate Visualizations (8 Key Findings)
import pandas as pd
import plotly.express as px

import sqlite3
conn = sqlite3.connect("phonepe.db")

# 1. Top Transaction Types
df1 = pd.read_sql("""
    SELECT transaction_type, SUM(amount) as total_amt
    FROM aggregated_transaction GROUP BY transaction_type
    ORDER BY total_amt DESC LIMIT 5
""", conn)
fig1 = px.bar(df1, x="total_amt", y="transaction_type", orientation='h',
              color="transaction_type", title="Top Transaction Types")
fig1.show()

# 2. Transaction Volume Over Time
df2 = pd.read_sql("""
    SELECT year, quarter, SUM(count) as txn_count
    FROM aggregated_transaction GROUP BY year, quarter
    ORDER BY year, quarter
""", conn)
df2['period'] = df2['year'].astype(str) + ' Q' + df2['quarter'].astype(str)
fig2 = px.line(df2, x="period", y="txn_count", markers=True,
               title="Transaction Volume Over Time")
fig2.show()

# 3. App Opens Per Quarter
df3 = pd.read_sql("""
    SELECT year, quarter, SUM(app_opens) as total_opens
    FROM aggregated_user_summary GROUP BY year, quarter
    ORDER BY year, quarter
""", conn)
df3['period'] = df3['year'].astype(str) + ' Q' + df3['quarter'].astype(str)
fig3 = px.area(df3, x="period", y="total_opens", title="App Opens Per Quarter")
fig3.show()

# 4. Registered Users Over Time
df4 = pd.read_sql("""
    SELECT year, quarter, SUM(registered_users) as users
    FROM aggregated_user_summary GROUP BY year, quarter
    ORDER BY year, quarter
""", conn)
df4['period'] = df4['year'].astype(str) + ' Q' + df4['quarter'].astype(str)
fig4 = px.line(df4, x="period", y="users", title="Registered Users Over Time")
fig4.show()

# 5. Top Devices Used
df5 = pd.read_sql("""
    SELECT brand, SUM(user_count) as total_users
    FROM aggregated_user_by_device GROUP BY brand
    ORDER BY total_users DESC LIMIT 5
""", conn)
fig5 = px.pie(df5, names="brand", values="total_users", title="Top 5 Devices Used")
fig5.show()

# 6. Average Transaction Amount Over Time
df6 = pd.read_sql("""
    SELECT year, quarter, SUM(amount)*1.0/SUM(count) as avg_txn_amt
    FROM aggregated_transaction GROUP BY year, quarter
    ORDER BY year, quarter
""", conn)
df6['period'] = df6['year'].astype(str) + ' Q' + df6['quarter'].astype(str)
fig6 = px.bar(df6, x="period", y="avg_txn_amt", title="Average Transaction Amount Over Time")
fig6.show()

# 7. Most Active Transaction Years
df7 = pd.read_sql("""
    SELECT year, SUM(count) as txn_count
    FROM aggregated_transaction GROUP BY year
    ORDER BY txn_count DESC
""", conn)
fig7 = px.bar(df7, x="year", y="txn_count", title="Most Active Transaction Years")
fig7.show()

# 8. Most Popular Quarters for App Opens
df8 = pd.read_sql("""
    SELECT quarter, SUM(app_opens) as total_opens
    FROM aggregated_user_summary GROUP BY quarter
    ORDER BY total_opens DESC
""", conn)
fig8 = px.funnel(df8, x="total_opens", y="quarter", title="Most Popular Quarters for App Opens")
fig8.show()

# Step - 5 Streamlit App Creation
app_code = '''
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

conn = sqlite3.connect("phonepe.db")
st.set_page_config(page_title="📊 PhonePe Insights", layout="wide")
st.title("📊 PhonePe Transaction Insights Dashboard")
st.subheader("8 Key Findings with Interactive Charts")

# 1. Top Transaction Types
df1 = pd.read_sql("SELECT transaction_type, SUM(amount) as total_amt FROM aggregated_transaction GROUP BY transaction_type ORDER BY total_amt DESC LIMIT 5", conn)
fig1 = px.bar(df1, x='transaction_type', y='total_amt', title="Top Transaction Types", color='transaction_type')
st.plotly_chart(fig1, use_container_width=True)

# 2. Transaction Volume Over Time
df2 = pd.read_sql("SELECT year, quarter, SUM(count) as txn_count FROM aggregated_transaction GROUP BY year, quarter ORDER BY year, quarter", conn)
df2['period'] = df2['year'].astype(str) + ' Q' + df2['quarter'].astype(str)
fig2 = px.line(df2, x='period', y='txn_count', title="Transaction Volume Over Time", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# 3. App Opens Per Quarter
df3 = pd.read_sql("SELECT year, quarter, SUM(app_opens) as total_opens FROM aggregated_user_summary GROUP BY year, quarter ORDER BY year, quarter", conn)
df3['period'] = df3['year'].astype(str) + ' Q' + df3['quarter'].astype(str)
fig3 = px.area(df3, x='period', y='total_opens', title="App Opens Per Quarter")
st.plotly_chart(fig3, use_container_width=True)

# 4. Registered Users Over Time
df4 = pd.read_sql("SELECT year, quarter, SUM(registered_users) as users FROM aggregated_user_summary GROUP BY year, quarter ORDER BY year, quarter", conn)
df4['period'] = df4['year'].astype(str) + ' Q' + df4['quarter'].astype(str)
fig4 = px.line(df4, x='period', y='users', title="Registered Users Over Time")
st.plotly_chart(fig4, use_container_width=True)

# 5. Top Devices Used
df5 = pd.read_sql("SELECT brand, SUM(user_count) as total_users FROM aggregated_user_by_device GROUP BY brand ORDER BY total_users DESC LIMIT 5", conn)
fig5 = px.pie(df5, names='brand', values='total_users', title="Top 5 Devices Used")
st.plotly_chart(fig5, use_container_width=True)

# 6. Average Transaction Amount Over Time
df6 = pd.read_sql("SELECT year, quarter, SUM(amount)*1.0/SUM(count) as avg_amt FROM aggregated_transaction GROUP BY year, quarter ORDER BY year, quarter", conn)
df6['period'] = df6['year'].astype(str) + ' Q' + df6['quarter'].astype(str)
fig6 = px.bar(df6, x='period', y='avg_amt', title="Avg. Transaction Amount Over Time")
st.plotly_chart(fig6, use_container_width=True)

# 7. Most Active Transaction Years
df7 = pd.read_sql("SELECT year, SUM(count) as txn_count FROM aggregated_transaction GROUP BY year ORDER BY txn_count DESC", conn)
fig7 = px.bar(df7, x='year', y='txn_count', title="Most Active Transaction Years")
st.plotly_chart(fig7, use_container_width=True)

# 8. Most Popular Quarters for App Opens
df8 = pd.read_sql("SELECT quarter, SUM(app_opens) as total_opens FROM aggregated_user_summary GROUP BY quarter ORDER BY total_opens DESC", conn)
fig8 = px.funnel(df8, x='total_opens', y='quarter', title="Most Popular Quarters for App Opens")
st.plotly_chart(fig8, use_container_width=True)

st.success("📈 Dashboard Loaded Successfully!")
'''
with open("app.py", "w") as f:
    f.write(app_code)

# Step 6 - Run Streamlit
from pyngrok import ngrok
import time
ngrok.set_auth_token("2z0Oqv0tD166fELGCHwV2gLZwq1_2G2zUQRSs6C27k9vdzxwq")

# Run Streamlit App in background
!streamlit run app.py &> /content/logs.txt &

# Wait for app to boot
time.sleep(5)

# Get public URL
public_url = ngrok.connect(8501)
print("🚀 Streamlit running at:", public_url)
