# **Implementing Delta Lake in Multi-Hop Architectures - Hands-on Labs**

## **Introduction**
This lab document provides a **detailed, step-by-step guide** to implementing a **Multi-Hop Architecture (Bronze, Silver, Gold layers)** using **Delta Lake**. These hands-on exercises focus on **real-world scenarios** using datasets such as **Bank Transactions, Loan Foreclosures, and Flight Data** to ensure practical learning with minimal modifications.

These labs cover:
- **Setting up Delta Lake multi-hop pipelines**
- **Ingesting data into the Bronze layer from Kafka and cloud storage**
- **Transforming data in the Silver layer (Cleansing, Deduplication, and CDC)**
- **Aggregating and curating data in the Gold layer**
- **Optimizing performance using Z-Ordering, Compaction, and Schema Enforcement**
- **Enabling Change Data Capture (CDC) and Time Travel**

Each lab provides **detailed code, execution steps, and validation techniques** to build **scalable, enterprise-ready data pipelines**.

---

## **Lab 1: Ingesting Data into the Bronze Layer**
### **Objective:**
- Load raw, unprocessed data into the **Bronze layer** from streaming and batch sources.

### **Step 1: Load Streaming Data from Kafka into the Bronze Layer**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("BronzeLayerIngestion").getOrCreate()

bronze_df = spark.readStream.format("kafka")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", "transactions")\
    .option("startingOffsets", "earliest")\
    .load()

bronze_df.writeStream.format("delta")\
    .option("checkpointLocation", "/mnt/delta/bronze_checkpoint")\
    .start("/mnt/delta/bronze_transactions")
```

### **Step 2: Load Batch Data from Cloud Storage**
```python
bronze_batch_df = spark.read.format("csv")\
    .option("header", "true")\
    .load("s3://my-bucket/raw-data/")

bronze_batch_df.write.format("delta").mode("append").save("/mnt/delta/bronze_transactions")
```

**Expected Outcome:**
- **Raw event-driven data is ingested into Delta Lake in append-only format.**

---

## **Lab 2: Processing and Cleaning Data in the Silver Layer**
### **Objective:**
- Deduplicate, clean, and transform the data **incrementally**.

### **Step 1: Load Bronze Data into Silver Layer**
```python
from delta.tables import DeltaTable

bronze_table = DeltaTable.forPath(spark, "/mnt/delta/bronze_transactions")

silver_df = bronze_table.toDF().dropDuplicates(["transaction_id"]).filter("amount IS NOT NULL")

silver_df.write.format("delta").mode("overwrite").save("/mnt/delta/silver_transactions")
```

### **Step 2: Enable Change Data Capture (CDC) for Incremental Processing**
```python
cdc_df = spark.readStream.format("delta")\
    .option("readChangeFeed", "true")\
    .table("silver_transactions")

query = cdc_df.writeStream.format("console").start()
query.awaitTermination()
```

**Expected Outcome:**
- **Silver layer contains cleaned, deduplicated data ready for business logic transformations.**
- **Incremental changes are continuously processed using CDC.**

---

## **Lab 3: Aggregating and Curating Data in the Gold Layer**
### **Objective:**
- Transform and **aggregate** cleansed data into business-ready tables.

### **Step 1: Perform Aggregations and Store Data in the Gold Layer**
```python
gold_df = spark.read.format("delta").load("/mnt/delta/silver_transactions")\
    .groupBy("customer_id", "transaction_date")\
    .agg({"amount": "sum"})\
    .withColumnRenamed("sum(amount)", "total_spent")

gold_df.write.format("delta").mode("overwrite").save("/mnt/delta/gold_transactions")
```

**Expected Outcome:**
- **Gold layer contains structured, aggregated data optimized for reporting and machine learning.**

---

## **Lab 4: Enabling Time Travel for Data Versioning**
### **Objective:**
- Query and restore previous data versions using **Time Travel**.

### **Step 1: Query a Previous Version of the Silver Layer**
```sql
SELECT * FROM silver_transactions VERSION AS OF 5;
```

### **Step 2: Restore a Table to a Previous Version**
```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "/mnt/delta/silver_transactions")
delta_table.restoreToVersion(3)
```

**Expected Outcome:**
- **Historical data versions are accessible for compliance, auditing, and rollback.**

---

## **Lab 5: Optimizing Performance with Compaction and Z-Ordering**
### **Objective:**
- Improve **query performance** and **reduce storage costs**.

### **Step 1: Compact Small Files Using OPTIMIZE**
```sql
OPTIMIZE gold_transactions;
```

### **Step 2: Improve Query Performance Using Z-Ordering**
```sql
OPTIMIZE gold_transactions ZORDER BY customer_id;
```

### **Step 3: Clean Up Old Data Versions Using VACUUM**
```sql
VACUUM silver_transactions RETAIN 24 HOURS;
```

**Expected Outcome:**
- **Improved query efficiency and reduced storage fragmentation.**

---

## **Lab 6: Automating Data Ingestion Using Auto Loader**
### **Objective:**
- Automate continuous ingestion from cloud storage.

### **Step 1: Configure Auto Loader to Monitor a Cloud Storage Path**
```python
raw_df = spark.readStream.format("cloudFiles")\
    .option("cloudFiles.format", "csv")\
    .option("cloudFiles.schemaLocation", "/mnt/delta/schema")\
    .load("s3://my-bucket/raw-data/")

raw_df.writeStream.format("delta")\
    .option("checkpointLocation", "/mnt/delta/autoloader_checkpoint")\
    .start("/mnt/delta/bronze_transactions")
```

**Expected Outcome:**
- **New files are automatically detected and processed.**

---

## **Conclusion**
By completing these **hands-on labs**, you have gained expertise in:
- **Building end-to-end Delta Lake pipelines using a multi-hop architecture.**
- **Processing raw data incrementally using CDC and schema enforcement.**
- **Optimizing Delta Lake tables for performance and cost efficiency.**
- **Automating data ingestion with Auto Loader.**
- **Ensuring data reliability with ACID transactions, time travel, and Z-Ordering.**

These labs provide **real-world experience** in building **scalable, fault-tolerant, and high-performance multi-hop architectures** that support **enterprise data lakes, analytics, and AI workloads**.

