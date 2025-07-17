
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
