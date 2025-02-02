# **Advanced Delta Table Optimizations and Constraints - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **step-by-step exercises** to apply advanced **Delta Table optimizations and constraints** for efficient data processing, storage management, and query performance. The following labs will cover:

- **Performance tuning using Z-Ordering, Partitioning, and Data Skipping**
- **Implementing Constraints (Primary Keys, NOT NULL, Check Constraints)**
- **Compaction techniques (OPTIMIZE) and Storage Retention (VACUUM)**
- **Indexing methods like Bloom Filters and Delta Caching**
- **Real-world scenarios using Bank Transactions, Loan Foreclosures, and Flights Data**

Each lab provides **detailed code, real-world examples, and validation steps** to ensure **scalable, high-performance Delta Lake operations**.

---

## **Lab 1: Applying Z-Ordering for Faster Query Performance**
### **Objective:**
- Improve query performance by **clustering frequently queried columns**.

### **Step 1: Load Bank Transactions Data into a Delta Table**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DeltaZOrderingLab").getOrCreate()

# Load sample Bank Transactions Data
data = [(101, "C001", 5000, "2024-01-01"),
        (102, "C002", 7000, "2024-01-02"),
        (103, "C001", 4500, "2024-01-03"),
        (104, "C003", 3000, "2024-01-04"),
        (105, "C002", 8000, "2024-01-05")]

columns = ["transaction_id", "customer_id", "amount", "transaction_date"]

df = spark.createDataFrame(data, columns)
df.write.format("delta").mode("overwrite").save("/mnt/delta/bank_transactions")
```

### **Step 2: Apply Z-Ordering Optimization**
```sql
OPTIMIZE delta.`/mnt/delta/bank_transactions` ZORDER BY (customer_id);
```

### **Step 3: Validate Optimization with Query Performance**
```sql
EXPLAIN FORMATTED SELECT * FROM bank_transactions WHERE customer_id = 'C001';
```

**Expected Outcome:**
- **Faster queries** on `customer_id` due to improved data locality.

---

## **Lab 2: Implementing Data Partitioning for Efficient Data Skipping**
### **Objective:**
- Reduce query scan time by **partitioning data based on transaction date**.

### **Step 1: Create a Partitioned Delta Table for Loan Foreclosure Data**
```sql
CREATE TABLE loan_foreclosures (
    loan_id STRING,
    customer_id STRING,
    outstanding_balance DOUBLE,
    foreclosure_date DATE
) USING DELTA
PARTITIONED BY (foreclosure_date);
```

### **Step 2: Load Data into the Partitioned Table**
```python
loan_df.write.format("delta").mode("overwrite").partitionBy("foreclosure_date").save("/mnt/delta/loan_foreclosures")
```

### **Step 3: Query Performance Validation**
```sql
SELECT * FROM loan_foreclosures WHERE foreclosure_date = '2024-01-01';
```

**Expected Outcome:**
- **Faster queries** by scanning only relevant partitions instead of the entire dataset.

---

## **Lab 3: Enforcing Data Integrity with Constraints**
### **Objective:**
- Apply **NOT NULL, Primary Key Simulations, and Check Constraints** to ensure data quality.

### **Step 1: Enforce NOT NULL Constraint on Flights Data**
```sql
ALTER TABLE flights ALTER COLUMN departure_time SET NOT NULL;
```

### **Step 2: Simulate a Primary Key using Merge**
```sql
MERGE INTO flights AS t
USING updates AS u
ON t.flight_id = u.flight_id
WHEN MATCHED THEN UPDATE SET t.status = u.status
WHEN NOT MATCHED THEN INSERT *;
```

### **Step 3: Add a Check Constraint for Flight Status**
```sql
ALTER TABLE flights ADD CONSTRAINT valid_status CHECK (status IN ('On Time', 'Delayed', 'Cancelled'));
```

**Expected Outcome:**
- **Prevention of null values** in `departure_time`.
- **Primary key simulation** ensures no duplicate `flight_id`.
- **Only valid flight statuses are allowed.**

---

## **Lab 4: Optimizing Storage with Compaction and Retention Policies**
### **Objective:**
- Improve **query performance** and **reduce small file overhead** using **OPTIMIZE and VACUUM**.

### **Step 1: Perform Compaction on Flights Data**
```sql
OPTIMIZE flights;
```

### **Step 2: Set Retention Policy and Clean Up Old Data**
```sql
VACUUM flights RETAIN 168 HOURS;
```

**Expected Outcome:**
- **Optimized query execution** with larger, fewer files.
- **Deleted old Delta versions** to free storage.

---

## **Lab 5: Implementing Bloom Filters for Indexing**
### **Objective:**
- Speed up **lookup queries** on `customer_id` using **Bloom Filters**.

### **Step 1: Enable Bloom Filter Indexing on Bank Transactions**
```sql
ALTER TABLE bank_transactions SET TBLPROPERTIES ('delta.bloomFilter.columns' = 'customer_id');
```

### **Step 2: Query and Compare Performance**
```sql
SELECT * FROM bank_transactions WHERE customer_id = 'C001';
```

**Expected Outcome:**
- **Significantly faster lookups** on `customer_id` due to indexed filtering.

---

## **Conclusion**
By completing these **hands-on labs**, you have gained expertise in:
- **Applying advanced Delta Lake optimizations** (Z-Ordering, Partitioning, and Data Skipping).
- **Ensuring data integrity using Constraints (NOT NULL, Check Constraints, Merge-based Primary Key simulation).**
- **Improving storage and query performance using Compaction and Retention policies.**
- **Leveraging Bloom Filters and Delta Caching for faster lookups.**

These labs provide **real-world experience** in building **scalable, high-performance Delta Lake solutions** for **enterprise analytics and real-time data processing**.

