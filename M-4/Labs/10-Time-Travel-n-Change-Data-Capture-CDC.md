# **Time Travel and Change Data Capture (CDC) - Hands-on Labs**

## **Introduction**
This lab document provides a **detailed, step-by-step guide** to implementing **Time Travel and Change Data Capture (CDC)** using **Apache Spark and Delta Lake**. These hands-on exercises will focus on **real-world scenarios**, utilizing datasets such as **Bank Transactions, Loan Foreclosures, and Flight Data** to ensure practical learning with minimal modifications.

These labs cover:
- **Implementing Time Travel to access historical data versions**
- **Restoring previous data states using Delta Lake**
- **Tracking and processing changes using CDC techniques**
- **Using Structured Streaming for real-time CDC pipelines**
- **Ensuring fault tolerance, exactly-once processing, and optimization**

Each lab provides **detailed code, execution steps, and validation techniques** to build **scalable, enterprise-ready data pipelines**.

---

## **Lab 1: Implementing Time Travel in Delta Lake**
### **Objective:**
- Enable **data versioning** and retrieve historical records.
- Restore data to a previous state using **Time Travel**.

### **Step 1: Create a Delta Table with Sample Data**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = SparkSession.builder.appName("TimeTravelLab").getOrCreate()

# Define sample transactions data
data = [(101, 5000, "2024-02-01"), (102, 7000, "2024-02-02"), (103, 4500, "2024-02-03")]
columns = ["transaction_id", "amount", "transaction_date"]

df = spark.createDataFrame(data, columns)
df.write.format("delta").mode("overwrite").save("/mnt/delta/transactions")
```

### **Step 2: Perform Updates and Check Versions**
```python
from delta.tables import DeltaTable

# Load Delta table
delta_table = DeltaTable.forPath(spark, "/mnt/delta/transactions")

# Update a record
delta_table.update("transaction_id = 101", {"amount": "6000"})

# Show history
delta_table.history().show()
```

### **Step 3: Query a Previous Version**
```python
previous_version = 0  # Adjust based on the output of history()
delta_df = spark.read.format("delta").option("versionAsOf", previous_version).load("/mnt/delta/transactions")
delta_df.show()
```

**Expected Outcome:**
- The previous transaction state should be retrieved using **Time Travel**.

---

## **Lab 2: Restoring Data to a Previous Version**
### **Objective:**
- Restore a table to a **specific historical version**.

### **Step 1: Restore Table to a Previous Version**
```python
restore_version = 1  # Choose an appropriate version from history()
delta_table.restoreToVersion(restore_version)
```

### **Step 2: Verify the Restoration**
```python
spark.read.format("delta").load("/mnt/delta/transactions").show()
```

**Expected Outcome:**
- The table should **roll back** to its previous state.

---

## **Lab 3: Implementing Change Data Capture (CDC) Using Merge**
### **Objective:**
- Implement **upserts and deletes** using CDC.

### **Step 1: Create Source Data with New Changes**
```python
updated_data = [(101, 5500, "2024-02-01"), (104, 9000, "2024-02-05")]  # New transaction
source_df = spark.createDataFrame(updated_data, columns)
source_df.write.format("delta").mode("overwrite").save("/mnt/delta/updates")
```

### **Step 2: Merge Updates into Target Table**
```python
source_table = DeltaTable.forPath(spark, "/mnt/delta/updates")
delta_table.alias("t").merge(
    source_table.alias("s"), "t.transaction_id = s.transaction_id"
).whenMatchedUpdate(set={"t.amount": "s.amount"})
 .whenNotMatchedInsert(values={"transaction_id": "s.transaction_id", "amount": "s.amount", "transaction_date": "s.transaction_date"})
 .execute()
```

### **Step 3: Verify the Changes**
```python
delta_table.toDF().show()
```

**Expected Outcome:**
- **Existing transactions should be updated, and new transactions should be inserted**.

---

## **Lab 4: Streaming CDC with Structured Streaming**
### **Objective:**
- Capture and process real-time updates using **Streaming CDC**.

### **Step 1: Enable Change Data Feed in Delta Lake**
```sql
ALTER TABLE transactions SET TBLPROPERTIES ('delta.enableChangeDataFeed' = true);
```

### **Step 2: Read CDC Data as a Stream**
```python
cdc_df = spark.readStream.format("delta")\
    .option("readChangeFeed", "true")\
    .table("transactions")

query = cdc_df.writeStream.format("console").start()
query.awaitTermination()
```

**Expected Outcome:**
- New changes should **stream continuously**.

---

## **Lab 5: Optimizing Time Travel and CDC Performance**
### **Objective:**
- Optimize **query performance** and **manage storage overhead**.

### **Step 1: Run Delta Optimization Commands**
```python
# Optimize table for performance
spark.sql("OPTIMIZE transactions")

# Clean old versions to reduce storage
spark.sql("VACUUM transactions RETAIN 30 HOURS")
```

**Expected Outcome:**
- Improved **query performance and reduced storage overhead**.

---

## **Conclusion**
By completing these **hands-on labs**, you have gained expertise in:
- **Querying and restoring historical data using Time Travel.**
- **Implementing Change Data Capture (CDC) with structured updates.**
- **Building streaming CDC pipelines for real-time analytics.**
- **Optimizing data lake performance using Delta Lake commands.**

These labs provide **real-world experience** in building **scalable, fault-tolerant, and high-performance data pipelines** for **enterprise-grade architectures**.

