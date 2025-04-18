# 🛒 Retail Sales Analysis using Apache Spark

This project performs **Big Data analysis** on a retail sales dataset using **Apache Spark** (PySpark). It includes data cleaning, exploratory analysis, SQL-based aggregation, performance optimization, and visualizations using Matplotlib and Seaborn.

## 📁 Dataset

- File: `retail_sales_dataset.csv`
- Contains retail transaction data including:
  - Transaction ID
  - Date
  - Customer ID
  - Gender
  - Age
  - Product Category
  - Quantity
  - Price per Unit
  - Total Amount

## ⚙️ Technologies Used

- Python 3.9+
- Apache Spark 3.3.2 (PySpark)
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook

## 📊 Analysis Performed

### ✅ Data Cleaning
- Removed rows with null values
- Removed duplicate records
- Converted `Quantity` and `Price per Unit` to numeric types
- Filtered out negative/invalid quantities or prices

### 🔍 Exploratory SQL Analysis
- **Revenue by Product Category**
- **Top Spending Customers**
- **Daily Revenue Trends**
- **(Optimized)** GroupBy operations with caching and repartitioning

### 📈 Visualizations
- **Bar Chart**: Revenue by Product Category
- **Line Chart**: Daily Sales Trend with weekend markers and peak annotations

### 🧠 Performance Optimization
- Cached cleaned DataFrame
- Repartitioned by `Customer ID` for parallelism
- Execution plan inspected with `.explain(True)`
- Timed group operations for performance monitoring

## 🏁 How to Run

1. Install required libraries:
   ```bash
   pip install pyspark==3.3.2 pandas matplotlib seaborn

2. Run the notebook:
 - jupyter notebook retail_sales_analysis.ipynb

## 📌 Project Highlights
 - Utilizes Apache Spark SQL for scalable query processing
 - Efficient handling of large datasets
 - Visually appealing and insightful charts
 - Performance-tuned transformations


## Author: Aquil Iqbal
## Course: Open Source Tools for Data Science
## Topic: Big Data Analysis using Apache Spark