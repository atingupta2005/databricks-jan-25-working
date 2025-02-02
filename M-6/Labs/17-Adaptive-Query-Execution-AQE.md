# **Adaptive Query Execution (AQE) - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **detailed, step-by-step exercises** to implement and optimize **Adaptive Query Execution (AQE)** in Apache Spark and **Databricks**. These labs will cover:
- **Enabling AQE and key configurations**
- **Optimizing shuffle partitions dynamically**
- **Implementing adaptive join strategies**
- **Handling data skew effectively**
- **Monitoring and troubleshooting AQE performance**

Each lab includes **real-world examples**, **step-by-step instructions**, and **sample dataset usage** (Banks Data, Loan Foreclosure Data, Flights Data from previous notebooks) to ensure **efficient query execution**.

---

## **Lab 1: Enabling AQE and Configurations**
### **Objective:**
- Enable and verify **Adaptive Query Execution (AQE)** in **Databricks**.

### **Step 1: Enable AQE in Databricks**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("AQE_Optimization") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

### **Step 2: Verify AQE Configuration**
```python
print("AQE Enabled:", spark.conf.get("spark.sql.adaptive.enabled"))
```

**Expected Outcome:**
- AQE is successfully **enabled** and **ready for execution optimizations**.

---

## **Lab 2: Optimizing Shuffle Partitions with AQE**
### **Objective:**
- Use **AQE to dynamically adjust shuffle partitions** based on data size.

### **Step 1: Load Sample Data** (Flights Data)
```python
df = spark.read.format("delta").load("abfss://datalake@storage.dfs.core.windows.net/flights_data")
```

### **Step 2: Enable Dynamic Shuffle Partitioning**
```python
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.minPartitionSize", "64MB")
```

### **Step 3: Execute and Observe Changes**
```python
result = df.groupBy("flight_id").count().collect()
print("Query Execution Completed Successfully")
```

**Expected Outcome:**
- Spark **dynamically adjusts** shuffle partitions to **optimize performance** and **reduce costs**.

---

## **Lab 3: Implementing Adaptive Join Strategies**
### **Objective:**
- Dynamically **switch join types** to optimize execution.

### **Step 1: Enable Adaptive Joins**
```python
spark.conf.set("spark.sql.adaptive.join.enabled", "true")
```

### **Step 2: Load Sample Datasets (Banks and Loan Data)**
```python
df_banks = spark.read.format("delta").load("abfss://datalake@storage.dfs.core.windows.net/banks_data")
df_loans = spark.read.format("delta").load("abfss://datalake@storage.dfs.core.windows.net/loan_foreclosure")
```

### **Step 3: Perform Join and Observe AQE Behavior**
```python
joined_df = df_loans.join(df_banks, "bank_id")
joined_df.show(5)
```

**Expected Outcome:**
- **AQE dynamically switches** from **shuffle join** to **broadcast join** when applicable, reducing shuffle overhead.

---

## **Lab 4: Handling Data Skew with AQE**
### **Objective:**
- Optimize queries by **handling data skew dynamically**.

### **Step 1: Enable Skew Join Optimization**
```python
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

### **Step 2: Load Skewed Data (Loan Foreclosure Data)**
```python
df_loans_skewed = spark.read.format("delta").load("abfss://datalake@storage.dfs.core.windows.net/loan_foreclosure_skewed")
```

### **Step 3: Execute Query and Monitor Execution Plan**
```python
from pyspark.sql.functions import col
result = df_loans_skewed.groupBy("loan_status").count()
result.explain(True)
```

**Expected Outcome:**
- AQE **automatically splits skewed partitions**, ensuring **better parallelism and query efficiency**.

---

## **Lab 5: Monitoring AQE Execution Plans**
### **Objective:**
- Understand **how AQE modifies query execution plans**.

### **Step 1: Enable AQE Execution Plan Logging**
```python
spark.conf.set("spark.sql.adaptive.logLevel", "INFO")
```

### **Step 2: Execute a Complex Query with AQE**
```python
df_complex = df_loans_skewed.groupBy("loan_purpose").agg({"loan_amount": "avg"})
df_complex.explain(True)
```

### **Step 3: Compare Execution Plan Changes**
- Observe **shuffle partition coalescing**.
- Identify **adaptive join strategy selection**.
- Check for **skew join optimizations**.

**Expected Outcome:**
- The execution plan **shows AQE optimizations**, proving its effectiveness in runtime tuning.

---

## **Conclusion**
By completing these **hands-on labs**, you have learned how to:
- **Enable and configure AQE** in **Databricks**.
- **Optimize shuffle partitions dynamically** to improve query performance.
- **Leverage adaptive join strategies** to reduce shuffle overhead.
- **Handle data skew automatically** to prevent slow-running queries.
- **Monitor and analyze AQE execution plans** for performance tuning.

These labs provide **real-world experience** in leveraging **Adaptive Query Execution (AQE) for Spark query optimization**, making **data processing faster, more efficient, and cost-effective**.

