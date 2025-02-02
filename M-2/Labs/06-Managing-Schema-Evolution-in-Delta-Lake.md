# **Managing Schema Evolution in Delta Lake - Hands-on Labs**

## **Introduction**
This lab document provides **detailed, step-by-step exercises** to help you master **schema evolution techniques** in **Delta Lake**. These hands-on labs focus on real-world scenarios, using **Bank Transactions, Loan Foreclosures, and Flight Data** as referenced in previous sample notebooks. These labs ensure **minimal changes for execution** and cover:

- **Schema enforcement and rejection of mismatched data**
- **Appending data with evolving schemas**
- **Merging schema changes dynamically**
- **Handling nested structures and complex schema modifications**
- **Implementing best practices for schema evolution in production**

Each lab includes **detailed code examples, step-by-step execution guidance, and validation checks**.

---

## **Lab 1: Understanding Schema Enforcement in Delta Lake**
### **Objective:**
- Learn how Delta Lake enforces schema consistency.
- Prevent accidental schema modifications.

### **Step 1: Create a Delta Table with a Fixed Schema**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SchemaEnforcementLab").getOrCreate()

# Load bank transactions dataset
bank_data_path = "/mnt/data/bank_transactions.csv"
bank_df = spark.read.csv(bank_data_path, header=True, inferSchema=True)

# Define schema
df = bank_df.select("transaction_id", "customer_id", "amount", "transaction_date")
df.write.format("delta").save("/mnt/delta/bank_transactions")
```

### **Step 2: Try Writing Data with a Different Schema**
```python
new_data = [(1001, 5002, 1500, "2024-05-01", "Online Purchase")]
df_new = spark.createDataFrame(new_data, ["transaction_id", "customer_id", "amount", "transaction_date", "transaction_type"])

df_new.write.format("delta").mode("append").save("/mnt/delta/bank_transactions")
```

**Expected Outcome:**
- The operation should fail due to schema mismatch.

---

## **Lab 2: Enabling Schema Evolution for Append Mode**
### **Objective:**
- Allow new columns to be added dynamically.

### **Step 1: Enable Schema Evolution in Write Operation**
```python
df_new.write.format("delta").option("mergeSchema", "true").mode("append").save("/mnt/delta/bank_transactions")
```

**Expected Outcome:**
- The table should now include the `transaction_type` column.
- Historical records should have `NULL` in the new column.

---

## **Lab 3: Handling Schema Evolution in Merge Operations**
### **Objective:**
- Manage schema evolution when merging updates.

### **Step 1: Create an Initial Loan Foreclosure Table**
```python
loan_data_path = "/mnt/data/loan_foreclosure.parquet"
loan_df = spark.read.parquet(loan_data_path)
loan_df.write.format("delta").save("/mnt/delta/loan_foreclosure")
```

### **Step 2: Merge Data with New Columns**
```python
new_data = [(105, "2024-06-15", 12000, "Pending Review")]
df_new = spark.createDataFrame(new_data, ["loan_id", "foreclosure_date", "amount", "review_status"])

from delta.tables import DeltaTable

loan_table = DeltaTable.forPath(spark, "/mnt/delta/loan_foreclosure")

loan_table.alias("t").merge(
    df_new.alias("s"), "t.loan_id = s.loan_id"").whenNotMatchedInsertAll()
.option("mergeSchema", "true").execute()
```

**Expected Outcome:**
- The `review_status` column should be added.

---

## **Lab 4: Schema Evolution in Nested and Struct Data**
### **Objective:**
- Manage schema changes in nested data.

### **Step 1: Create a Delta Table with Nested Columns**
```python
from pyspark.sql.functions import struct

data = [(1, struct("John", "Doe"), "NY", "Regular Customer")]
df = spark.createDataFrame(data, ["customer_id", "name", "city", "customer_category"])
df.write.format("delta").save("/mnt/delta/customers_nested")
```

### **Step 2: Append Data with a New Field in Struct**
```python
new_data = [(2, struct("Alice", "Smith", "VIP"), "LA", "High Net Worth")]
df_new = spark.createDataFrame(new_data, ["customer_id", "name", "city", "customer_category"])
df_new.write.format("delta").option("mergeSchema", "true").mode("append").save("/mnt/delta/customers_nested")
```

**Expected Outcome:**
- The `name` struct should now include a `VIP` category.

---

## **Lab 5: Schema Evolution in Streaming Data**
### **Objective:**
- Handle schema drift in structured streaming.

### **Step 1: Simulate a Streaming Data Source**
```python
flight_data_path = "/mnt/data/flights.parquet"
streaming_df = spark.readStream.format("delta").load("/mnt/delta/flights")
```

### **Step 2: Enable Schema Evolution for Streaming Writes**
```python
new_stream_data = [(207, "2024-07-10", "Delayed", "Weather Issue")]
df_new = spark.createDataFrame(new_stream_data, ["flight_id", "flight_date", "status", "delay_reason"])

df_new.writeStream.format("delta").option("mergeSchema", "true").outputMode("append").start("/mnt/delta/flights")
```

**Expected Outcome:**
- The `delay_reason` column should be dynamically added without affecting streaming pipelines.

---

## **Conclusion**
By completing these hands-on labs, you have gained expertise in:
- **Schema enforcement and preventing unintended schema changes.**
- **Handling schema evolution dynamically using append and merge operations.**
- **Managing schema modifications in nested and struct columns.**
- **Ensuring seamless schema evolution in structured streaming workflows.**

These labs provide **real-world experience** in schema evolution using **Delta Lake**, ensuring data pipelines remain **scalable, reliable, and flexible**.

