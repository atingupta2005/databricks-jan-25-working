# **Automating Jobs with CI/CD Pipelines - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **detailed, step-by-step exercises** for implementing **CI/CD pipelines** in **data engineering and machine learning workflows** using **Databricks, Terraform, GitHub Actions, and Azure DevOps**.

These labs will cover:
- **Setting up version control for Databricks notebooks and data workflows**.
- **Automating testing and validation of Spark jobs, Delta Lake pipelines, and ML models**.
- **Deploying Databricks jobs using GitHub Actions and Azure DevOps**.
- **Infrastructure as Code (IaC) for managing Databricks clusters and resources**.
- **Monitoring, error handling, and security best practices in CI/CD pipelines**.
- **Using existing datasets (Banks Data, Loan Foreclosure Data, Flights Data) from previous notebooks to ensure real-world relevance.**

Each lab includes **real-world examples**, **step-by-step instructions**, and **sample dataset usage** to ensure **scalability and reliability**.

---

## **Lab 1: Setting Up Version Control for Databricks Notebooks**
### **Objective:**
- Learn how to integrate **Databricks Workflows** with **GitHub/Azure DevOps**.

### **Step 1: Enable Git Integration in Databricks**
1. Open **Databricks Workspace** → Navigate to **Repos**.
2. Click **Add Repo** → Select **GitHub/Azure DevOps**.
3. Connect to a GitHub repository with your **notebooks and scripts**.

### **Step 2: Clone a Repository into Databricks**
```bash
databricks repos create --url https://github.com/my-org/databricks-repo --path /Repos/my-repo
```

### **Step 3: Commit and Push Changes from Databricks to Git**
```bash
git add .
git commit -m "Updated ETL notebooks"
git push origin main
```

**Expected Outcome:**
- Databricks notebooks are **version-controlled in GitHub/Azure DevOps**.

---

## **Lab 2: Automating Testing and Validation in CI/CD Pipelines**
### **Objective:**
- Implement **automated testing** for **Spark jobs and Delta Lake ingestion pipelines**.

### **Step 1: Install Great Expectations for Data Validation**
```python
pip install great_expectations
```

### **Step 2: Validate a Delta Lake Table Schema (Using Flights Data)**
```python
import great_expectations as ge
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataValidation").getOrCreate()
df = spark.read.format("delta").load("abfss://datalake@storage.dfs.core.windows.net/flights_data")

df_expectations = ge.dataset.SparkDFDataset(df)
assert df_expectations.expect_column_values_to_not_be_null("flight_id").success
assert df_expectations.expect_column_to_exist("departure_time").success
```

### **Step 3: Automate Testing in CI/CD Pipeline**
Modify **GitHub Actions YAML** to run tests on every push:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2
      - name: Run Data Validation
        run: python validate_data.py
```

**Expected Outcome:**
- The test will **fail if missing values** exist in `flight_id` or `departure_time`.
- CI/CD pipeline ensures **data integrity before processing**.

---

## **Lab 3: Deploying Databricks Jobs Using GitHub Actions**
### **Objective:**
- Automate **Databricks job deployments** using **GitHub Actions**.

### **Step 1: Create a Job JSON Config**
```json
{
  "name": "Loan Foreclosure ETL",
  "new_cluster": {
    "spark_version": "11.3.x-scala2.12",
    "num_workers": 3
  },
  "notebook_task": {
    "notebook_path": "/Repos/databricks-repo/loan_foreclosure_etl"
  }
}
```

### **Step 2: Deploy the Job Using GitHub Actions**
Modify the CI/CD pipeline to deploy the job:
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Deploy Databricks Job
        run: databricks jobs create --json-file job_config.json
```

**Expected Outcome:**
- Databricks **automatically executes the ETL pipeline** when new data is available.

---

## **Lab 4: Infrastructure as Code (IaC) for Databricks Using Terraform**
### **Objective:**
- Provision Databricks **clusters and job workflows** using Terraform.

### **Step 1: Create a Terraform Configuration for a Cluster (Banks Data Processing)**
```hcl
resource "databricks_cluster" "banks_cluster" {
  cluster_name = "Banks Data Processing"
  spark_version = "11.3.x-scala2.12"
  num_workers = 4
}
```

### **Step 2: Apply Terraform Configuration**
```bash
terraform init
terraform apply -auto-approve
```

**Expected Outcome:**
- A **Databricks cluster** is automatically provisioned to handle **Banks Data Processing**.

---

## **Lab 5: Implementing Monitoring and Error Handling in CI/CD**
### **Objective:**
- Enable **logging, monitoring, and failure handling** in CI/CD pipelines.

### **Step 1: Configure Logging in Databricks Jobs**
```python
import logging
logger = logging.getLogger("ci-cd-pipeline")
logger.setLevel(logging.INFO)
logger.info("Processing started for Loan Foreclosure Data")
```

### **Step 2: Implement Retry Logic in CI/CD Workflows**
Modify **GitHub Actions YAML** to include **automatic retries**:
```yaml
jobs:
  deploy:
    steps:
      - name: Retry Databricks Job Deployment
        run: |
          for i in {1..3}; do
            databricks jobs run-now --job-id 7890 && break || sleep 60;
          done
```

**Expected Outcome:**
- Job failures **trigger alerts**, and **retry logic** ensures automatic reattempts.

---

## **Conclusion**
By completing these **hands-on labs**, you have learned how to:
- **Automate Databricks workflows using GitHub Actions and Azure DevOps**.
- **Implement automated testing for data pipelines using real-world datasets**.
- **Provision infrastructure using Terraform**.
- **Enable monitoring, alerts, and retry logic in CI/CD workflows**.

These labs provide **real-world experience** in **deploying production-ready data engineering pipelines** using **CI/CD best practices**.

