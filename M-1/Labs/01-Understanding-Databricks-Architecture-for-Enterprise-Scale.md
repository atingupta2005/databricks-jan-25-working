# Lab Guide: Understanding Databricks Architecture for Enterprise Scale (Azure)

## **Objective**
This hands-on lab will focus on **real-world, production-ready implementations** of Databricks on **Azure**. You will:
- Configure an **Azure Databricks workspace**.
- Set up **Azure Data Lake Storage Gen2 (ADLS)** and manage secure access.
- Build **real-world ETL workflows** using **Delta Lake**.
- Automate data pipelines with **Azure Databricks Jobs**.
- Optimize performance using **adaptive query execution (AQE) and Photon Engine**.
- Implement **real-world** use cases based on previously provided sample datasets.

## **Prerequisites**
- **Azure Subscription** with permissions to create resources.
- **Azure Databricks workspace** and **Azure Storage Account** with ADLS Gen2.
- **Service Principal** for secure authentication.
- **Familiarity with Apache Spark, Python, and SQL.**

---

## **Lab 1: Configuring Azure Databricks for Secure Enterprise Data Processing**

### **Step 1: Create an Azure Databricks Workspace**
1. Navigate to **Azure Portal** → **Create a Resource** → Search `Azure Databricks`.
2. Click **Create** and configure:
   - **Subscription**: Select an existing subscription.
   - **Resource Group**: Create a new one or use an existing one.
   - **Workspace Name**: `enterprise-databricks`
   - **Region**: Select the closest data region.
   - **Pricing Tier**: **Premium** (for RBAC, security, and governance).
3. Click **Review + Create**, then deploy the workspace.

### **Step 2: Deploy a High-Performance Databricks Cluster**
1. Navigate to **Compute** → **Create Cluster**.
2. Configure:
   - **Cluster Mode**: Standard
   - **Databricks Runtime**: **Photon-Enabled ML Runtime**
   - **Worker Type**: `Standard_D8ds_v4`
   - **Auto-scaling**: Min **3**, Max **12** workers
   - **Enable Adaptive Query Execution (AQE)**
3. Click **Create Cluster** and wait for it to initialize.

### **Step 3: Attach a Notebook to the Cluster**
1. Go to **Workspace** → **Create** → **Notebook**.
2. Choose **Python** as the default language.
3. Attach the notebook to your **Databricks cluster**.
4. Run the following command:
   ```python
   from pyspark.sql import SparkSession
   spark = SparkSession.builder.appName("Enterprise_Azure_Databricks").getOrCreate()
   print(spark.version)
   ```

---

## **Lab 2: Secure Data Access with Azure Data Lake (ADLS Gen2)**

### **Step 1: Create an Azure Storage Account and Container**
1. Open **Azure Portal** → **Storage Accounts** → **Create**.
2. Configure:
   - **Storage Account Name**: `databricks-adls-gen2`
   - **Enable Hierarchical Namespace**: **Yes**
   - **Enable Secure Transfer**: **Yes**
3. Click **Create**.
4. Navigate to **Containers** → **Create New** → Name: `enterprise-data`.

### **Step 2: Authenticate Using a Service Principal**
```python
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": "<Application_Client_ID>",
           "fs.azure.account.oauth2.client.secret": "<Client_Secret>",
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<Tenant_ID>/oauth2/token"}

# Mount ADLS Storage
dbutils.fs.mount(source="abfss://enterprise-data@databricks-adls-gen2.dfs.core.windows.net/", 
                 mount_point="/mnt/adls_enterprise", 
                 extra_configs=configs)

print(dbutils.fs.ls("/mnt/adls_enterprise"))
```
Replace placeholders with your actual values.

---

## **Lab 3: Real-World ETL Processing with Delta Lake**

### **Step 1: Create and Optimize Delta Tables**
```python
# Load sample data from ADLS
adls_path = "/mnt/adls_enterprise/raw_transactions.csv"
df = spark.read.csv(adls_path, header=True, inferSchema=True)

# Convert to Delta format
df.write.format("delta").mode("overwrite").save("/mnt/adls_enterprise/delta/transactions")
```

### **Step 2: Optimize Performance Using Z-Ordering**
```sql
OPTIMIZE delta.`/mnt/adls_enterprise/delta/transactions` ZORDER BY (transaction_id);
```

---

## **Lab 4: Automating Enterprise Data Pipelines**

### **Step 1: Create an Azure Databricks Job**
```python
job_config = {
    "name": "Daily_Transaction_Processing",
    "tasks": [
        {
            "task_key": "load_delta_table",
            "notebook_task": {
                "notebook_path": "/Workspace/ETL/transaction_processing"
            },
            "existing_cluster_id": "<Cluster_ID>"
        }
    ]
}
dbutils.notebook.run("/Workspace/ETL/transaction_processing", 0)
```
Replace `<Cluster_ID>` with your cluster ID.

---

## **Lab 5: Advanced Performance Optimization**

### **Use Adaptive Query Execution (AQE)**
```python
spark.conf.set("spark.sql.adaptive.enabled", True)
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", True)
spark.conf.set("spark.sql.adaptive.localShuffleReader.enabled", True)
```

### **Leverage Photon Engine for Faster Query Execution**
```sql
SELECT customer_id, SUM(amount) AS total_spent
FROM delta.`/mnt/adls_enterprise/delta/transactions`
GROUP BY customer_id
ORDER BY total_spent DESC;
```

---

## **Conclusion**
This lab provided a **real-world, enterprise-grade approach** to deploying **Azure Databricks**, securely integrating with **Azure Data Lake**, implementing **ETL pipelines with Delta Lake**, automating workflows, and optimizing performance using **AQE and Photon Engine**.

By following this guide, enterprises can build **highly scalable, secure, and production-ready** data architectures on **Azure Databricks**.

