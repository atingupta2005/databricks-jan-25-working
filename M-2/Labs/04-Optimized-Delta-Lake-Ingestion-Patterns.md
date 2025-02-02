# **Delta Lake Ingestion: Hands-on Labs**

## **Introduction**
This lab guide provides **detailed, step-by-step hands-on exercises** to optimize **Delta Lake ingestion patterns**. These labs ensure **high-performance, scalable, and cost-efficient data ingestion** workflows. Each lab is designed to work with **minimal changes**, using **variables and configurations** for flexibility.

By completing these labs, you will gain experience in:
1. **Batch and Streaming Data Ingestion into Delta Lake**
2. **Optimizing Write Performance using Partitioning, Z-Ordering, and Auto-Optimized Writes**
3. **Schema Evolution and Enforced Data Consistency**
4. **Managing Incremental Data and Change Data Capture (CDC)**
5. **Storage Management with Auto-Compaction, Vacuum, and Time Travel**
6. **Real-World Use Cases with Detailed Implementation**

---

## **Lab 1: Ingesting Batch and Streaming Data into Delta Lake**

### **Step 1: Initialize Spark Session and Set Up Variables**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DeltaLakeIngestion").getOrCreate()

# Define storage paths
base_path = "/mnt/delta/"
raw_data_path = "/mnt/raw_data/"
checkpoint_path = "/mnt/checkpoints/"

# Define table names
delta_table_name = "user_events"
```

### **Step 2: Batch Data Ingestion using Append Mode**
```python
# Sample batch data
data = [("user_1", "login", "2024-01-01"), ("user_2", "purchase", "2024-01-02")]
df = spark.createDataFrame(data, ["user_id", "event_type", "event_date"])

# Writing to Delta Lake in Append mode
df.write.format("delta").mode("append").save(f"{base_path}{delta_table_name}")
```

### **Step 3: Streaming Data Ingestion using Structured Streaming**
```python
streaming_df = spark.readStream.format("json").schema("user_id STRING, event_type STRING, event_date STRING").load(raw_data_path)

streaming_df.writeStream.format("delta")\
    .option("checkpointLocation", f"{checkpoint_path}logs/")\
    .start(f"{base_path}logs")
```

---

## **Lab 2: Optimizing Write Performance with Partitioning and Z-Ordering**

### **Step 1: Writing Data with Partitioning**
```python
df.write.format("delta").partitionBy("event_date").save(f"{base_path}partitioned_events")
```

### **Step 2: Optimizing Reads using Z-Ordering**
```sql
OPTIMIZE delta.`/mnt/delta/events` ZORDER BY (event_type);
```

---

## **Lab 3: Schema Evolution and Enforced Data Consistency**

### **Step 1: Enabling Schema Evolution**
```python
df.write.format("delta").option("mergeSchema", "true").mode("append").save(f"{base_path}schema_evolution")
```

### **Step 2: Enforcing Schema on Write**
```sql
ALTER TABLE delta_table ADD COLUMN new_column STRING;
```

---

## **Lab 4: Managing Incremental Data and Change Data Capture (CDC)**

### **Step 1: Merging Incremental Data Efficiently**
```sql
MERGE INTO transactions AS target
USING new_transactions AS source
ON target.transaction_id = source.transaction_id
WHEN MATCHED THEN
  UPDATE SET target.amount = source.amount, target.status = source.status
WHEN NOT MATCHED THEN
  INSERT (transaction_id, amount, status, timestamp) VALUES (source.transaction_id, source.amount, source.status, source.timestamp);
```

### **Step 2: Using Change Data Capture (CDC) Queries**
```sql
SELECT * FROM delta_table WHERE _change_type = 'update_postimage';
```

---

## **Lab 5: Optimizing Query Performance and Storage Management**

### **Step 1: Enabling Auto-Optimized Writes**
```python
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", True)
```

### **Step 2: Enabling Automatic File Compaction**
```python
spark.conf.set("spark.databricks.delta.autoCompact.enabled", True)
```

### **Step 3: Retaining Historical Data using Time Travel**
```sql
SELECT * FROM delta.`/mnt/delta/events` VERSION AS OF 10;
```

### **Step 4: Deleting Old Data with VACUUM**
```sql
VACUUM delta.`/mnt/delta/events` RETAIN 7 HOURS;
```

---

## **Lab 6: Real-World Use Cases and Implementations**

### **Use Case 1: Real-Time Security Log Ingestion and Processing**

#### **Scenario:** A cybersecurity firm ingests **millions of log events per second** for **real-time threat detection**.

#### **Implementation:**
```python
log_df = spark.readStream.format("json").load(f"{raw_data_path}security_logs/")

log_df.writeStream.format("delta")\
    .partitionBy("log_source", "event_date")\
    .option("checkpointLocation", f"{checkpoint_path}security_logs/")\
    .start(f"{base_path}security_logs")
```

---

### **Use Case 2: Banking Transaction Upserts with CDC**

#### **Scenario:** A financial institution **processes real-time transactions** and ensures **data consistency**.

#### **Implementation:**
```sql
MERGE INTO bank_transactions AS target
USING new_transactions AS source
ON target.transaction_id = source.transaction_id
WHEN MATCHED THEN
  UPDATE SET target.amount = source.amount, target.status = source.status
WHEN NOT MATCHED THEN
  INSERT (transaction_id, amount, status, timestamp) VALUES (source.transaction_id, source.amount, source.status, source.timestamp);
```

---

### **Use Case 3: ETL Pipeline for E-Commerce Data Processing**

#### **Scenario:** An e-commerce company needs to process **customer actions in real-time** and **refresh product catalog daily**.

#### **Implementation:**
```python
# Process customer activity logs in real-time
customer_logs_df = spark.readStream.format("json").load(f"{raw_data_path}ecommerce/logs/")

customer_logs_df.writeStream.format("delta")\
    .option("checkpointLocation", f"{checkpoint_path}ecommerce/")\
    .start(f"{base_path}ecommerce_logs")

# Refresh product catalog daily
daily_catalog_df = spark.read.format("json").load(f"{raw_data_path}ecommerce/product_catalog/")

daily_catalog_df.write.format("delta").mode("overwrite").save(f"{base_path}product_catalog")
```

---

## **Conclusion**
By completing these labs, you will **master optimized Delta Lake ingestion patterns** and build **scalable, high-performance, and cost-efficient** data pipelines in **Databricks**.

