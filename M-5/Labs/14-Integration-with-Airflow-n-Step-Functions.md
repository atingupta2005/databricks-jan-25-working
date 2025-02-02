# **Integration with Airflow and Step Functions - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **detailed, step-by-step exercises** for building, managing, and optimizing **workflow orchestration** using **Apache Airflow and AWS Step Functions**. These labs cover:
- **Creating Apache Airflow DAGs for Databricks job orchestration**
- **Triggering workflows dynamically using event-based execution**
- **Building AWS Step Functions state machines to automate workflows**
- **Error handling, retries, and monitoring execution logs**
- **Real-world integration with Databricks, Azure, and AWS services**
- **Using existing datasets such as Banks Data, Loan Foreclosure Data, and Flights Data from previous notebooks**

Each lab includes **real-world examples, step-by-step instructions, sample dataset usage, and advanced workflow orchestration techniques** to build **scalable and production-ready workflows**.

---

## **Lab 1: Orchestrating a Databricks Job using Apache Airflow**
### **Objective:**
- Define an **Airflow DAG** to run a **Databricks job** in **Azure Databricks**.

### **Step 1: Install Required Packages in Airflow**
```bash
pip install apache-airflow-providers-databricks
```

### **Step 2: Create an Airflow DAG to Trigger a Databricks Job Using Bank Transactions Data**
```python
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG(
    "bank_transactions_databricks_orchestration",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

run_databricks_job = DatabricksRunNowOperator(
    task_id="trigger_bank_transactions_processing",
    job_id="5678",
    databricks_conn_id="databricks_default",
    dag=dag,
)

run_databricks_job
```

### **Step 3: Deploy and Monitor the DAG in Airflow**
1. Save the DAG as `bank_transactions_airflow_dag.py` in the Airflow DAGs folder.
2. Restart the Airflow scheduler to detect the new DAG.
3. Open the **Airflow UI**, enable the DAG, and trigger a manual run.
4. Check the **Logs & Execution Status**.

**Expected Outcome:**
- Airflow DAG successfully triggers a **Databricks job processing bank transactions data** and completes execution.

---

## **Lab 2: Automating a Loan Foreclosure Data Pipeline with Apache Airflow**
### **Objective:**
- Automate ETL workflows for **Loan Foreclosure Data** with **Databricks** and **Airflow**.

### **Step 1: Define a DAG for Loan Data Processing**
```python
from airflow.operators.dummy import DummyOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

dag = DAG(
    "loan_foreclosure_processing",
    default_args=default_args,
    schedule_interval="0 2 * * *",  # Runs daily at 2 AM UTC
    catchup=False,
)

start = DummyOperator(task_id="start_task", dag=dag)
process_loan_data = DatabricksRunNowOperator(
    task_id="run_loan_data_etl",
    job_id="9102",
    databricks_conn_id="databricks_default",
    dag=dag,
)
start >> process_loan_data
```

**Expected Outcome:**
- The workflow **extracts, transforms, and loads loan foreclosure data into Databricks Delta Lake**.

---

## **Lab 3: Automating Workflows using AWS Step Functions**
### **Objective:**
- Create an **AWS Step Functions** state machine that processes **Flights Data** and sends alerts for delayed flights.

### **Step 1: Define the AWS Step Functions State Machine**
```json
{
  "Comment": "A Step Function to process flight delay data",
  "StartAt": "TriggerFlightProcessing",
  "States": {
    "TriggerFlightProcessing": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:triggerFlightsProcessing",
      "Next": "CheckForDelays"
    },
    "CheckForDelays": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.delay_status",
          "StringEquals": "Delayed",
          "Next": "SendAlert"
        }
      ],
      "Default": "EndState"
    },
    "SendAlert": {
      "Type": "Task",
      "Resource": "arn:aws:sns:us-east-1:123456789012:SendDelayAlert",
      "End": true
    },
    "EndState": {
      "Type": "Pass",
      "End": true
    }
  }
}
```

**Expected Outcome:**
- The **Step Function processes flight delays** and **triggers an alert if a flight is delayed**.

---

## **Lab 4: Implementing Advanced Error Handling and Logging in Workflows**
### **Objective:**
- Implement **robust retry logic and logging mechanisms** in **Airflow DAGs and AWS Step Functions**.

### **Step 1: Enable Logging and Retry Logic in Airflow DAG**
```python
from airflow.exceptions import AirflowFailException
from airflow.decorators import task

@task(retries=3, retry_delay=timedelta(minutes=10))
def unreliable_task():
    import random
    if random.choice([True, False]):
        raise AirflowFailException("Simulated failure")
    return "Task Succeeded"
```

### **Step 2: Enable Logging in AWS Step Functions**
1. Open **AWS Step Functions Console** → Select a State Machine Execution.
2. Click on **Execution History** to track each step.
3. Enable **CloudWatch Logs** for real-time monitoring.

**Expected Outcome:**
- **Workflows retry failed tasks up to 3 times before marking them as failed**.
- **CloudWatch and Airflow logs provide detailed insights for debugging**.

---

## **Conclusion**
By completing these **hands-on labs**, you have gained expertise in:
- **Orchestrating Databricks workflows with Apache Airflow.**
- **Automating Loan Foreclosure and Flight Data Pipelines.**
- **Implementing error handling, retries, and logging in workflows.**
- **Using AWS Step Functions for event-driven automation.**

These labs provide **real-world experience** in **building robust, scalable workflow automation solutions** for **enterprise-scale data pipelines**.

