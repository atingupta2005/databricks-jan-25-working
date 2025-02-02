# **Building Fault-Tolerant Streaming Pipelines - Hands-on Labs**

## **Introduction**
This lab document provides **detailed, step-by-step exercises** to help you master **fault tolerance in streaming pipelines** using **Apache Spark Structured Streaming and Delta Lake**. These labs focus on real-world datasets such as **Bank Transactions, Loan Foreclosures, and Flight Data** as referenced in previous sample notebooks.

These labs will cover:
- **Ensuring recovery using Checkpointing & Write-Ahead Logging (WAL)**
- **Guaranteeing exactly-once processing with idempotent writes**
- **Handling late-arriving data using watermarks**
- **Managing backpressure and autoscaling for high availability**
- **Monitoring, debugging, and failure recovery in streaming pipelines**

Each lab provides **detailed code examples, execution steps, and validation checks** to ensure practical and scalable solutions.

---

## **Lab 1: Implementing Checkpointing and WAL for Fault Tolerance**
### **Objective:**
- Ensure **fault recovery** using **checkpointing and WAL**.
- Resume streaming jobs from the last successful state.

### **Step 1: Set Up Streaming Data Source (Bank Transactions)**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("FaultToleranceLab1").getOrCreate()

# Load bank transactions dataset
bank_data_path = "/mnt/data/bank_transactions.csv"
bank_schema = "transaction_id INT, customer_id INT, amount FLOAT, transaction_date STRING"
bank_df = spark.readStream.format("csv").option("header", "true").schema(bank_schema).load(bank_data_path)
```

### **Step 2: Configure Checkpointing and WAL**
```python
query = bank_df.writeStream.format("delta")\
    .option("checkpointLocation", "/mnt/delta/bank_checkpoint")\
    .outputMode("append")\
    .start("/mnt/delta/bank_transactions")
```

**Expected Outcome:**
- If the job crashes and restarts, it should **resume from the last committed checkpoint**.
- **No duplicate records** should be written.

---

## **Lab 2: Ensuring Exactly-Once Processing with Idempotent Writes**
### **Objective:**
- Prevent duplicate records when recovering from failures.
- Use **Delta Lake's ACID transactions** to maintain consistency.

### **Step 1: Define a Streaming Query with Idempotent Writes**
```python
from delta.tables import DeltaTable

def upsert_to_delta(microBatchDF, batchId):
    deltaTable = DeltaTable.forPath(spark, "/mnt/delta/bank_transactions")
    deltaTable.alias("t").merge(
        microBatchDF.alias("s"), "t.transaction_id = s.transaction_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

query = bank_df.writeStream.format("delta")\
    .foreachBatch(upsert_to_delta)\
    .option("checkpointLocation", "/mnt/delta/bank_checkpoint")\
    .outputMode("update")\
    .start()
```

**Expected Outcome:**
- **Duplicate transactions are prevented**.
- **Idempotent writes ensure consistent state across restarts**.

---

## **Lab 3: Handling Late Data with Watermarks**
### **Objective:**
- Process late-arriving transactions while ensuring correctness.
- Prevent outdated records from affecting aggregations.

### **Step 1: Define a Watermark for Late Transactions**
```python
from pyspark.sql.functions import window

bank_df_with_watermark = bank_df.withWatermark("transaction_date", "10 minutes")

agg_query = bank_df_with_watermark.groupBy(
    window("transaction_date", "10 minutes"), "customer_id"
).agg({"amount": "sum"})

query = agg_query.writeStream.format("delta")\
    .option("checkpointLocation", "/mnt/delta/bank_checkpoint")\
    .outputMode("append")\
    .start("/mnt/delta/bank_aggregated")
```

**Expected Outcome:**
- Late transactions arriving **within 10 minutes** of their event-time are processed correctly.
- Older transactions are **discarded**, avoiding incorrect computations.

---

## **Lab 4: Managing Backpressure & Autoscaling**
### **Objective:**
- Prevent overload using **backpressure handling**.
- Enable **autoscaling** in Spark streaming jobs.

### **Step 1: Configure Backpressure Settings**
```python
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.streaming.backpressure.enabled", "true")
spark.conf.set("spark.streaming.kafka.maxRatePerPartition", "100")
```

### **Step 2: Enable Autoscaling in Databricks**
- **Go to Databricks Cluster Settings**
- **Enable Autoscaling** and set min/max worker nodes.

**Expected Outcome:**
- Spark **adjusts micro-batch sizes dynamically** based on system load.
- Autoscaling **adds/removes worker nodes** automatically during traffic spikes.

---

## **Lab 5: Monitoring & Debugging Streaming Failures**
### **Objective:**
- Implement **real-time monitoring** and **failure recovery mechanisms**.

### **Step 1: Enable Streaming Metrics**
```python
query = bank_df.writeStream.format("console")\
    .trigger(processingTime="10 seconds")\
    .option("truncate", "false")\
    .start()
```

### **Step 2: Enable Logs for Debugging Failures**
- **Check Databricks UI > Streaming** for real-time monitoring.
- **View Spark Event Logs** to analyze failures.
- **Enable cluster-level logs** for deeper insights.

**Expected Outcome:**
- Streaming metrics display **processing rates, backpressure indicators, and failure logs**.
- Logs capture **detailed stack traces** for debugging.

---

## **Conclusion**
By completing these **hands-on labs**, you have gained expertise in:
- **Implementing checkpointing and WAL for fault tolerance.**
- **Ensuring exactly-once processing with idempotent writes.**
- **Handling late-arriving data with watermarks.**
- **Managing backpressure and enabling autoscaling for resilience.**
- **Monitoring and debugging streaming failures for high availability.**

These labs provide **real-world experience** in **building fault-tolerant streaming pipelines**, ensuring that enterprises can process real-time data **with high reliability and consistency**.

