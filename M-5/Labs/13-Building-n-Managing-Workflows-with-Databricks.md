# **Building and Managing Workflows with Databricks Workflows - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **detailed, step-by-step exercises** for building, managing, and optimizing **Databricks Workflows**. These labs will cover:
- **Creating Databricks Jobs and Tasks**
- **Defining task dependencies and execution order**
- **Automating ETL and ML pipelines using Databricks Workflows**
- **Scheduling workflows using triggers and event-based execution**
- **Monitoring and handling workflow errors**
- **Optimizing execution time and cost efficiency**
- **Using sample data from Bank Transactions, Loan Foreclosure Data, and Flights Data**

Each lab provides **real-world scenarios**, **detailed execution steps**, **sample data usage**, and **expected outcomes** to build **scalable and production-ready workflows**.

---

## **Lab 1: Creating a Simple Databricks Workflow**
### **Objective:**
- Learn how to create a **Databricks Job** and define **multiple tasks**.

### **Step 1: Create a New Job**
1. Navigate to **Workflows > Jobs** in Databricks.
2. Click **Create Job**.
3. Name the job: `ETL_Pipeline_Workflow`.

### **Step 2: Define Tasks Using Real Data (Flights Data)**
1. Click **Add Task** and choose **Notebook Task**.
2. Set **Task Name**: `Extract_Flights_Data`.
3. Choose a **Cluster** and **Notebook Path** (`/Users/etl/extract_flights_data`).
4. Click **Add Task** again to create a new task:
   - **Task Name**: `Transform_Flights_Data`
   - **Depends on**: `Extract_Flights_Data`
   - **Notebook Path**: `/Users/etl/transform_flights_data`
5. Add another task:
   - **Task Name**: `Load_Flights_to_Delta`
   - **Depends on**: `Transform_Flights_Data`
   - **Notebook Path**: `/Users/etl/load_flights_delta`

### **Step 3: Run and Monitor the Workflow**
1. Click **Run Now**.
2. Navigate to the **Runs** tab and track execution.

**Expected Outcome:**
- The workflow **executes tasks sequentially**, ensuring **dependency management** for processing flights data.

---

## **Lab 2: Automating an ETL Pipeline using Databricks Workflows**
### **Objective:**
- Build an **ETL pipeline** that extracts, transforms, and loads **Bank Transactions Data** into **Delta Lake**.

### **Step 1: Define an ETL Job with Tasks**
```json
{
  "name": "ETL_Pipeline",
  "tasks": [
    {"task_key": "ingest_bronze", "notebook_task": {"notebook_path": "./bronze_ingest_bank_data"}},
    {"task_key": "transform_silver", "depends_on": [{"task_key": "ingest_bronze"}], "notebook_task": {"notebook_path": "./silver_transform_bank_data"}},
    {"task_key": "aggregate_gold", "depends_on": [{"task_key": "transform_silver"}], "notebook_task": {"notebook_path": "./gold_aggregate_bank_data"}}
  ]
}
```

### **Step 2: Execute the ETL Workflow**
```python
from databricks.sdk import JobsClient
jobs_api = JobsClient()
jobs_api.create(job_payload)
```

**Expected Outcome:**
- The workflow **automates an ETL pipeline**, storing **processed bank transaction data in Delta Lake**.

---

## **Lab 3: Scheduling Workflows Using Triggers**
### **Objective:**
- Automate workflow execution using **time-based and event-driven triggers**.

### **Step 1: Configure a Time-Based Trigger for Loan Foreclosure Data**
1. Open the **ETL_Pipeline** job in Databricks Workflows.
2. Click **Add Trigger** → Select **Scheduled**.
3. Choose **Cron Expression**: `0 0 */6 * * ?` (Runs every 6 hours).
4. Save and enable the schedule.

### **Step 2: Configure an Event-Based Trigger for New Loan Data Arrival**
1. Open the **ETL_Pipeline** job.
2. Click **Add Trigger** → Select **File Arrival**.
3. Choose **Cloud Storage Location**: `abfss://my-container@my-storage-account.dfs.core.windows.net/loan-data/`.
4. Enable the trigger.

**Expected Outcome:**
- **Loan data is processed every 6 hours** and **whenever new loan data arrives in S3**.

---

## **Lab 4: Error Handling and Retry Mechanisms**
### **Objective:**
- Implement **error handling** and **automatic retries** in Databricks Workflows.

### **Step 1: Configure Retry Logic**
```json
{
  "task": {
    "max_retries": 3,
    "min_retry_interval_millis": 60000,
    "retry_on_timeout": true
  }
}
```

### **Step 2: Enable Alerts on Failure**
1. Open **ETL_Pipeline** job.
2. Click **Add Alert** → Select **Failure Condition**.
3. Choose **Notification Method** (Email, Slack, PagerDuty).
4. Save the alert.

**Expected Outcome:**
- **Tasks automatically retry up to 3 times** before failure.
- **Alerts notify users on job failures.**

---

## **Lab 5: Optimizing Workflow Performance and Cost**
### **Objective:**
- Improve workflow efficiency by optimizing **cluster configurations**.

### **Step 1: Configure Cluster for Cost Efficiency**
1. Open **ETL_Pipeline** job.
2. Click **Edit Cluster** → Enable **Auto-Termination (5 min idle timeout)**.
3. Choose **Spot Instances** for cost optimization.

### **Step 2: Enable Delta Caching for Faster Execution**
```python
spark.conf.set("spark.databricks.io.cache.enabled", "true")
```

**Expected Outcome:**
- **Lower costs** due to **auto-termination and spot instances**.
- **Faster execution** using **Delta Caching**.

---

## **Conclusion**
By completing these **hands-on labs**, you have gained expertise in:
- **Creating and managing Databricks Workflows**.
- **Building automated ETL and ML pipelines**.
- **Using scheduling triggers for workflow automation**.
- **Implementing error handling and monitoring workflows**.
- **Optimizing execution time and cost efficiency**.

These labs provide **real-world experience** in **building production-ready workflows** for **enterprise-scale data and AI workloads**, leveraging **Flights Data, Bank Transactions, and Loan Foreclosure Data**.

