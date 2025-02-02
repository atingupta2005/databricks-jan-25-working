# **Advanced Transformation Techniques with PySpark - Hands-on Labs**

## **Introduction**
This **comprehensive hands-on lab guide** provides **detailed, step-by-step instructions** for applying **advanced transformation techniques in PySpark** using **real-world datasets such as Bank Transactions, Loan Foreclosures, and Flight Data** (as used in previous sample notebooks). These labs are designed to ensure **minimal changes** are required for execution and cover:

- **Lazy evaluation & DAG execution**
- **Data preprocessing & schema evolution**
- **Complex aggregations & window functions**
- **Optimized joins & broadcast techniques**
- **Handling complex nested data**
- **Performance tuning in PySpark**

Each lab provides **real-world datasets**, **in-depth explanations**, and **detailed code** to ensure **efficient and scalable big data processing**.

---

## **Lab 1: Understanding Lazy Evaluation & DAG Execution**
### **Objective:**
- Learn how PySpark transformations execute lazily.
- Visualize execution plans and DAG (Directed Acyclic Graph).

### **Step 1: Load Bank Transactions Data**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("LazyEvaluationLab").getOrCreate()

# Load bank transaction dataset
bank_df = spark.read.csv("/mnt/data/bank_transactions.csv", header=True, inferSchema=True)
bank_df.show(5)
```

### **Step 2: Apply Transformations Without Execution**
```python
filtered_df = bank_df.filter(bank_df.amount > 5000)
selected_df = filtered_df.select("transaction_id", "amount", "account_type")
```

### **Step 3: Trigger Execution & Inspect DAG**
```python
selected_df.show(10)
print(selected_df.explain(True))
```
**Expected Outcome:**
- DAG should confirm execution only after an action is triggered.

---

## **Lab 2: Data Preprocessing & Schema Evolution**
### **Objective:**
- Handle missing values, duplicates, and schema changes.

### **Step 1: Load Loan Foreclosure Data**
```python
loan_df = spark.read.parquet("/mnt/data/loan_foreclosure.parquet")
loan_df.printSchema()
loan_df.show(5)
```

### **Step 2: Handle Missing Values**
```python
loan_cleaned = loan_df.na.fill({"credit_score": 650, "income": 50000})
loan_cleaned.show(5)
```

### **Step 3: Schema Evolution - Merging New Data**
```python
new_loans_df = spark.createDataFrame([(12345, "NewLoan", 750, 70000, "Approved")],
                                      ["loan_id", "loan_type", "credit_score", "income", "status"])

merged_loans = loan_df.unionByName(new_loans_df, allowMissingColumns=True)
merged_loans.show()
```

---

## **Lab 3: Complex Aggregations & Window Functions**
### **Objective:**
- Use window functions for running totals, ranks, and trend analysis.

### **Step 1: Load Flight Data**
```python
flight_df = spark.read.parquet("/mnt/data/flights.parquet")
flight_df.show(5)
```

### **Step 2: Compute Total Flights per Airline**
```python
from pyspark.sql.functions import count

total_flights = flight_df.groupBy("airline").agg(count("flight_id").alias("total_flights"))
total_flights.show()
```

### **Step 3: Apply Window Functions to Rank Delays**
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import rank

window_spec = Window.partitionBy("airline").orderBy(flight_df.delay.desc())
flight_df = flight_df.withColumn("rank", rank().over(window_spec))
flight_df.show(10)
```

---

## **Lab 4: Optimized Joins & Broadcast Techniques**
### **Objective:**
- Learn efficient join strategies and use broadcast joins.

### **Step 1: Load Bank Customer & Transaction Data**
```python
customers_df = spark.read.csv("/mnt/data/bank_customers.csv", header=True, inferSchema=True)
transactions_df = spark.read.csv("/mnt/data/bank_transactions.csv", header=True, inferSchema=True)
```

### **Step 2: Perform a Join on Customer Transactions**
```python
joined_df = customers_df.join(transactions_df, "customer_id", "inner")
joined_df.show(5)
```

### **Step 3: Use Broadcast Join for Optimization**
```python
from pyspark.sql.functions import broadcast

optimized_df = transactions_df.join(broadcast(customers_df), "customer_id", "inner")
optimized_df.show(5)
```

---

## **Lab 5: Handling Complex Nested Data**
### **Objective:**
- Process struct, array, and map-based data.

### **Step 1: Load Nested Loan Data**
```python
nested_loan_df = spark.read.json("/mnt/data/nested_loan_data.json")
nested_loan_df.show(truncate=False)
```

### **Step 2: Extract Struct Fields**
```python
nested_loan_df.select("loan_details.interest_rate", "loan_details.duration").show()
```

### **Step 3: Flattening Arrays**
```python
from pyspark.sql.functions import explode

exploded_loans = nested_loan_df.withColumn("customer_loan", explode("loan_history"))
exploded_loans.select("customer_id", "customer_loan.*").show()
```

---

## **Lab 6: Performance Tuning & Optimization**
### **Objective:**
- Optimize PySpark workloads using caching, partitioning, and execution plans.

### **Step 1: Caching & Persisting Data**
```python
loan_cleaned.cache()
loan_cleaned.count()  # Triggers cache storage
```

### **Step 2: Inspect Execution Plans**
```python
loan_cleaned.explain(True)
```

### **Step 3: Managing Partitions for Scalability**
```python
optimized_loans = loan_cleaned.repartition("loan_status")
```

---

## **Conclusion**
By completing these **exhaustive hands-on labs**, you will have mastered:
- **Lazy evaluation & DAG execution**
- **Data preprocessing & schema evolution**
- **Complex aggregations & window functions**
- **Optimized joins & broadcast techniques**
- **Handling complex nested data structures**
- **Performance tuning for large-scale datasets**

These labs provide **enterprise-grade real-world experience** in handling **banking, loan foreclosure, and flight data** using **PySpark's advanced transformations**, ensuring **optimized and scalable big data workflows**.

