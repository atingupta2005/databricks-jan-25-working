# **Enabling Data Lineage and Auditing with Unity Catalog - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **detailed, step-by-step exercises** to implement **data lineage and auditing using Unity Catalog in Databricks**. These labs will cover:
- **Enabling and verifying data lineage tracking**.
- **Auditing data access and modifications**.
- **Querying lineage metadata for compliance and impact analysis**.
- **Best practices for managing lineage and audit logs**.

Each lab includes **real-world examples**, **step-by-step instructions**, and **SQL queries** to ensure **secure and transparent data governance**.

---

## **Lab 1: Enabling and Viewing Data Lineage in Unity Catalog**
### **Objective:**
- Enable and validate **automatic data lineage tracking** in Unity Catalog.

### **Step 1: Register a Table in Unity Catalog**
```sql
CREATE TABLE unity_catalog.sales_data (
    order_id STRING,
    customer_id STRING,
    order_date DATE,
    amount DECIMAL(10,2)
) USING DELTA;
```

### **Step 2: Perform Data Transformations**
```sql
CREATE TABLE unity_catalog.aggregated_sales AS
SELECT customer_id, SUM(amount) AS total_spent
FROM unity_catalog.sales_data
GROUP BY customer_id;
```

### **Step 3: View Lineage in Databricks UI**
1. Open **Databricks Unity Catalog**.
2. Navigate to **sales_data** table.
3. Click the **Lineage Tab** to see transformations.

**Expected Outcome:**
- **Table-level and column-level lineage** is displayed in Unity Catalog.

---

## **Lab 2: Querying Lineage Metadata for Compliance**
### **Objective:**
- Use **system tables** to query lineage metadata.

### **Step 1: Retrieve Lineage Information**
```sql
SELECT * FROM system.information_schema.table_lineage
WHERE table_name = 'aggregated_sales';
```

### **Step 2: Identify Upstream and Downstream Dependencies**
```sql
SELECT upstream_table, downstream_table, column_lineage
FROM system.information_schema.column_lineage
WHERE downstream_table = 'aggregated_sales';
```

**Expected Outcome:**
- The queries return **all transformations and dependencies** for the specified table.

---

## **Lab 3: Enabling and Configuring Audit Logging in Unity Catalog**
### **Objective:**
- Enable **audit logging** to track user activity.

### **Step 1: Enable Databricks Audit Logs in Azure**
1. Open **Azure Portal** → Navigate to **Azure Monitor**.
2. Select **Diagnostic Settings** for your Databricks workspace.
3. Enable **Audit Logs** and configure storage in **Azure Blob Storage** or **Event Hub**.

### **Step 2: Verify Logging Configuration**
- Run the following command to check if audit logs are enabled:
```bash
az monitor diagnostic-settings list --resource <databricks_workspace_id>
```

**Expected Outcome:**
- **Audit logs are being stored** in the configured location.

---

## **Lab 4: Querying Audit Logs for Data Access Tracking**
### **Objective:**
- Identify **who accessed data and when**.

### **Step 1: Query Data Access Logs**
```sql
SELECT user_name, action, table_name, event_time
FROM system.information_schema.audit_logs
WHERE action IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE')
ORDER BY event_time DESC;
```

### **Step 2: Investigate Unauthorized Access Attempts**
```sql
SELECT user_name, action, table_name, event_time
FROM system.information_schema.audit_logs
WHERE action = 'DENIED';
```

**Expected Outcome:**
- The logs display **who accessed which tables** and **any denied access attempts**.

---

## **Lab 5: Setting Up Alerts for Unauthorized Access**
### **Objective:**
- Configure **alerts for unauthorized data access**.

### **Step 1: Create an Alert in Azure Monitor**
1. Open **Azure Monitor** → Click **Alerts**.
2. Create a **New Alert Rule**.
3. Set condition: **Log query → Filter action = 'DENIED'**.
4. Set action: **Send Email Notification to Security Team**.

**Expected Outcome:**
- An alert is triggered whenever **unauthorized access** is attempted.

---

## **Conclusion**
By completing these **hands-on labs**, you have learned how to:
- **Enable data lineage tracking** in Unity Catalog.
- **Query lineage metadata to track transformations**.
- **Configure and analyze audit logs for security monitoring**.
- **Set up alerts for unauthorized data access attempts**.

These labs provide **real-world experience** in enforcing **data transparency, governance, and security best practices** in **Databricks and cloud environments**.

