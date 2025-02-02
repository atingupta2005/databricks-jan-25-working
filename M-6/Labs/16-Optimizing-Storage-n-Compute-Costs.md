# **Optimizing Storage and Compute Costs - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **detailed, step-by-step exercises** for optimizing **storage and compute costs** in **Databricks, Azure, and AWS environments**. These labs cover:
- **Efficient data storage using Delta Lake, Parquet, and lifecycle management**.
- **Optimizing compute usage through cluster tuning, auto-scaling, and serverless computing**.
- **Monitoring and governing costs using cloud-native tools and alerts**.

Each lab includes **real-world examples**, **step-by-step instructions**, and **sample dataset usage** (Banks Data, Loan Foreclosure Data, Flights Data from previous notebooks) to ensure **scalability and reliability**.

---

## **Lab 1: Implementing Delta Lake for Storage Optimization**
### **Objective:**
- Reduce **storage costs and query time** by using **Delta Lake** for efficient data storage.

### **Step 1: Create a Delta Table**
```python
from delta.tables import *
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DeltaOptimization").getOrCreate()

# Load Data
df = spark.read.format("csv").option("header", "true").load("abfss://datalake@storage.dfs.core.windows.net/flights_data")

# Convert to Delta Lake
df.write.format("delta").mode("overwrite").save("abfss://datalake@storage.dfs.core.windows.net/delta/flights")
```

### **Step 2: Enable Delta File Compaction**
```python
deltaTable = DeltaTable.forPath(spark, "abfss://datalake@storage.dfs.core.windows.net/delta/flights")
deltaTable.optimize().executeCompaction()
```

**Expected Outcome:**
- Delta Lake **reduces small files**, improving query efficiency and reducing storage costs.

---

## **Lab 2: Using Parquet Format to Reduce Storage Costs**
### **Objective:**
- Use **columnar storage formats** like **Parquet** to minimize storage costs.

### **Step 1: Convert CSV to Parquet**
```python
df.write.format("parquet").mode("overwrite").save("abfss://datalake@storage.dfs.core.windows.net/parquet/flights")
```

### **Step 2: Compare File Sizes**
```bash
# List storage files to compare sizes
az storage blob list --container-name datalake --account-name myaccount --query "[].{Name:name, Size:properties.contentLength}"
```

**Expected Outcome:**
- **Parquet files are smaller than CSV**, reducing storage costs while maintaining fast query performance.

---

## **Lab 3: Implementing Auto-Scaling for Compute Optimization**
### **Objective:**
- Automatically **adjust cluster size** based on workload demand to reduce costs.

### **Step 1: Configure Auto-Scaling in Databricks**
```json
{
  "cluster_name": "Optimized Cluster",
  "autoscale": {
    "min_workers": 2,
    "max_workers": 8
  }
}
```

### **Step 2: Monitor Auto-Scaling Performance**
- Open **Databricks UI** → Navigate to **Clusters**.
- Observe the cluster **scaling up/down** based on workload.

**Expected Outcome:**
- Cluster **scales dynamically**, reducing compute costs when idle and handling peak loads efficiently.

---

## **Lab 4: Enabling Serverless Computing to Minimize Costs**
### **Objective:**
- Run **serverless queries** on demand, paying only for execution time.

### **Step 1: Enable Serverless SQL Warehouse in Databricks**
```json
{
  "warehouse_type": "serverless",
  "enable_auto_stop": true
}
```

### **Step 2: Run a Serverless Query**
```sql
SELECT COUNT(*) FROM delta.`abfss://datalake@storage.dfs.core.windows.net/delta/flights`;
```

**Expected Outcome:**
- **No persistent compute resources**, significantly reducing idle compute costs.

---

## **Lab 5: Implementing Cost Monitoring and Alerts**
### **Objective:**
- Set up **cost monitoring tools** and **alerts** to track and control expenses.

### **Step 1: Configure Azure Cost Alerts**
```json
{
  "conditions": {
    "metricName": "StorageUsedGB",
    "threshold": 5000
  },
  "actionGroup": "SendEmailAlert"
}
```

### **Step 2: Enable Cost Reports in Azure Cost Management**
1. Open **Azure Portal** → Go to **Cost Management + Billing**.
2. Navigate to **Cost Analysis** and set up a **custom budget alert**.

**Expected Outcome:**
- Teams receive **alerts** when storage or compute usage exceeds predefined thresholds.

---

## **Conclusion**
By completing these **hands-on labs**, you have learned how to:
- **Optimize storage using Delta Lake and Parquet formats**.
- **Minimize compute costs with auto-scaling and serverless computing**.
- **Implement real-time cost monitoring and governance policies**.

These labs provide **real-world experience** in building **cost-effective and scalable data workflows** while maintaining performance and reliability.

