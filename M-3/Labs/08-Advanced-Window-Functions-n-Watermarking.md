# **Advanced Window Functions and Watermarking - Hands-on Labs**

## **Introduction**
This lab document provides **detailed, step-by-step exercises** to help you master **window functions and watermarking in Apache Spark Structured Streaming**. The labs focus on real-world datasets such as **Bank Transactions, Loan Foreclosures, and Flight Data**, as referenced in previous sample notebooks. These labs ensure **minimal changes for execution** and follow best practices for **state management, efficiency, and correctness**.

These labs will cover:
- **Implementing Tumbling, Sliding, and Session Windows**
- **Using Watermarks to Handle Late-Arriving Data Efficiently**
- **Combining Windows and Watermarks for Reliable Aggregations**
- **Optimizing Query Performance and State Management**
- **Monitoring and Debugging Streaming Windows**

Each lab provides **detailed code examples, execution steps, and validation checks** to ensure practical and scalable solutions with **real-world complexity**.

---

## **Lab 1: Implementing Tumbling Windows for Transaction Aggregation**
### **Objective:**
- Perform transaction count and sum over fixed time windows.
- Ensure state efficiency while handling high-throughput data.

### **Step 1: Load Streaming Data (Bank Transactions)**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col

spark = SparkSession.builder.appName("TumblingWindowLab").getOrCreate()

# Define source path for bank transactions
bank_data_path = "/mnt/data/bank_transactions.csv"

# Define schema for structured streaming
bank_schema = """
    transaction_id INT,
    customer_id INT,
    amount FLOAT,
    transaction_type STRING,
    transaction_date TIMESTAMP
"""

# Read stream
bank_df = spark.readStream\
    .format("csv")\
    .option("header", "true")\
    .schema(bank_schema)\
    .load(bank_data_path)
```

### **Step 2: Apply Tumbling Window Aggregation**
```python
tumbling_window_df = bank_df.withWatermark("transaction_date", "10 minutes")\
    .groupBy(window("transaction_date", "10 minutes"), "transaction_type")\
    .agg({"amount": "sum", "transaction_id": "count"})\
    .withColumnRenamed("sum(amount)", "total_amount")\
    .withColumnRenamed("count(transaction_id)", "transaction_count")
```

### **Step 3: Write Streaming Output to Delta Lake**
```python
query = tumbling_window_df.writeStream\
    .format("delta")\
    .option("checkpointLocation", "/mnt/delta/bank_checkpoint")\
    .outputMode("append")\
    .start("/mnt/delta/bank_transactions_windowed")
```

**Expected Outcome:**
- Transactions are grouped into **non-overlapping 10-minute intervals**.
- Each interval outputs **transaction count and total amount by transaction type.**

---

## **Lab 2: Implementing Sliding Windows for Flight Delay Monitoring**
### **Objective:**
- Calculate rolling flight delay averages using sliding windows.
- Capture overlapping time windows for real-time analytics.

### **Step 1: Load Streaming Data (Flight Delays)**
```python
from pyspark.sql.functions import avg

flight_data_path = "/mnt/data/flights.parquet"
flight_schema = "flight_id INT, airline STRING, delay INT, event_time TIMESTAMP"

flight_df = spark.readStream.format("parquet").schema(flight_schema).load(flight_data_path)
```

### **Step 2: Apply Sliding Window Aggregation**
```python
sliding_window_df = flight_df.withWatermark("event_time", "15 minutes")\
    .groupBy(window("event_time", "15 minutes", "5 minutes"), "airline")\
    .agg(avg("delay").alias("average_delay"))
```

### **Step 3: Write Streaming Output to Console**
```python
query = sliding_window_df.writeStream\
    .format("console")\
    .outputMode("update")\
    .start()
```

**Expected Outcome:**
- Flight delays are averaged over **overlapping 15-minute windows sliding every 5 minutes**.
- The same flight may appear in multiple overlapping windows.

---

## **Lab 3: Using Session Windows for E-Commerce User Sessionization**
### **Objective:**
- Dynamically track user sessions based on inactivity timeout.
- Optimize memory utilization by discarding stale session states.

### **Step 1: Load Streaming Data (User Activity Logs)**
```python
from pyspark.sql.functions import session_window

user_data_path = "/mnt/data/user_activity.json"
user_schema = "user_id STRING, action STRING, event_time TIMESTAMP"

user_df = spark.readStream.format("json").schema(user_schema).load(user_data_path)
```

### **Step 2: Apply Session Window Aggregation**
```python
session_window_df = user_df.withWatermark("event_time", "30 minutes")\
    .groupBy(session_window("event_time", "30 minutes"), "user_id")\
    .count()
```

### **Step 3: Write Streaming Output to Delta Lake**
```python
query = session_window_df.writeStream\
    .format("delta")\
    .option("checkpointLocation", "/mnt/delta/user_session_checkpoint")\
    .outputMode("append")\
    .start("/mnt/delta/user_sessions")
```

**Expected Outcome:**
- User sessions are **dynamically grouped based on 30-minute inactivity.**
- Sessionized data is stored efficiently using **Delta Lake for further analysis.**

---

## **Conclusion**
By completing these **hands-on labs**, you have gained expertise in:
- **Using Tumbling, Sliding, and Session Windows for real-time aggregations**.
- **Applying watermarks to manage late-arriving data efficiently**.
- **Combining windows and watermarks for optimal streaming performance**.
- **Ensuring state efficiency and data accuracy in real-time event processing**.
- **Writing streaming output to Delta Lake for persistence and analytics**.

These labs provide **real-world experience** in **window functions and watermarking**, ensuring scalable and reliable **structured streaming pipelines** that handle **high-volume, real-time data efficiently**.

