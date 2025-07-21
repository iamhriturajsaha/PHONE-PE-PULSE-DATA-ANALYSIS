# 📊 PhonePe Pulse Data Analysis
---

> An end-to-end data analytics project on PhonePe Pulse data, leveraging SQL, Python and Streamlit for interactive insights into digital payment trends across India.
---

## 🧠 Overview

This project aims to extract, analyze, and visualize PhonePe Pulse data to uncover transaction patterns, user engagement and regional trends in digital payments. The insights are displayed through an interactive dashboard built with Streamlit and hosted via ngrok on Google Colab.
---

## 🚀 Skills Highlighted

- Data Extraction & Cleaning  
- SQL Querying & Data Modeling  
- Python Programming & EDA  
- Interactive Visualizations (Plotly, Seaborn, Matplotlib)  
- Streamlit Dashboard Development  
- Business Insight Generation  
- ETL (Extract, Transform, Load)
---

## 📌 Problem Statement

With the rise of digital payment platforms like PhonePe, it's crucial to:
- Understand transaction behaviors.
- Track user growth and engagement.
- Monitor state/district-wise transaction volumes.
- Identify trends and generate actionable business insights.
---

## 🧩 Project Structure

### 1. 📂 Data Extraction
- Cloned the [PhonePe Pulse GitHub repository](https://github.com/PhonePe/pulse).
- Extracted nested JSON files for transaction and user data.

### 2. 🧱 SQL Database Setup
Created and populated the following tables in SQLite -

#### Aggregated Tables
- `aggregated_transaction`
- `aggregated_user_summary`
- `aggregated_user_by_device`

#### Map Tables
- (Planned) State- and district-level map visualizations

#### Top Tables
- (Planned) Insights into top states, districts, pin codes by metrics

### 3. 🧮 Data Analysis
- Executed SQL queries to analyze transactions by -
  - Year, Quarter, State
  - Device brand, User engagement
- Python used for -
  - Data wrangling (`pandas`)
  - Visualizations (`seaborn`, `matplotlib`, `plotly`)

### 4. 📊 Dashboard with Streamlit
- Built an interactive web dashboard in Streamlit
- Hosted directly from Google Colab via `pyngrok`
---

## 📈 Insights & Findings

- Identified **top-performing states** and **high-volume districts**
- Observed **seasonal and quarterly growth** patterns
- Analyzed **device brand preferences** across regions
- Measured **user growth vs app engagement** over time
---

## 🧪 Evaluation Metrics

| Metric              | Description |
|---------------------|-------------|
| ✅ Code Quality       | Follows Python & SQL best practices |
| ⚡ SQL Efficiency     | Fast and accurate queries |
| 📊 Visualization Clarity | Meaningful and intuitive plots |
| 🧠 Insight Validity    | Actionable, business-relevant findings |
| 📚 Documentation      | Thorough and well-structured |
---

## 🔧 Tools & Technologies

![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 🖼️ Streamlit

Here are some snapshots of the interactive dashboard built using Streamlit -

<p align="center">
  <img src="Streamlit Images/1.png" alt="Streamlit Dashboard 1" width="700"/><br>
  <img src="Streamlit Images/2.png" alt="Streamlit Dashboard 2" width="700"/><br>
  <img src="Streamlit Images/3.png" alt="Streamlit Dashboard 3" width="700"/><br>
  <img src="Streamlit Images/4.png" alt="Streamlit Dashboard 4" width="700"/><br>
  <img src="Streamlit Images/5.png" alt="Streamlit Dashboard 5" width="700"/>
</p>
