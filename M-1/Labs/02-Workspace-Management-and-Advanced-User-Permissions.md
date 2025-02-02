# **Databricks Workspace Management & Advanced User Permissions - Lab Guide**

## **Introduction**
This lab guide provides a **detailed hands-on approach** to managing workspaces, configuring user permissions, enforcing security policies, and automating Databricks access controls at an **enterprise level**.

By completing these labs, you will learn how to:
1. **Create and manage users, groups, and roles** programmatically and via UI.
2. **Assign permissions using Unity Catalog for enterprise-wide governance.**
3. **Configure and test row-level security, column masking, and access control lists.**
4. **Automate workspace setup using APIs, Terraform, and Databricks CLI.**
5. **Implement enterprise security policies like MFA, IP whitelisting, and logging.**
6. **Monitor and audit workspace activity for compliance enforcement.**
7. **Manage Databricks workflows, clusters, and job permissions dynamically.**

These labs **simulate real-world enterprise use cases**, ensuring **practical hands-on proficiency** in workspace security and governance.

---

## **Lab 1: User, Group & Role Management in Databricks**

### **Step 1: Adding Users via UI**
1. Navigate to **Databricks Admin Console**.
2. Click **User Management → Add User**.
3. Enter the user's email address.
4. Assign a role:
   - `Workspace Admin`
   - `Data Engineer`
   - `Data Scientist`
   - `Analyst`
5. Click **Create User**.

### **Step 2: Creating Groups & Assigning Users**
1. Navigate to **Groups → Create New Group**.
2. Name the group (e.g., `Data Engineers`).
3. Add users to the group.
4. Assign **cluster, notebook, and job permissions** to the group.
5. Click **Create**.

### **Step 3: Managing Users & Groups via API**
```python
import requests
TOKEN = "<DATABRICKS_ACCESS_TOKEN>"
DATABRICKS_URL = "https://<databricks-instance>.cloud.databricks.com/api/2.0/groups/list"
headers = {"Authorization": f"Bearer {TOKEN}"}
response = requests.get(DATABRICKS_URL, headers=headers)
print(response.json())
```

---

## **Lab 2: Unity Catalog - Fine-Grained Access Control**

### **Step 1: Granting Table-Level Access**
```sql
GRANT SELECT ON TABLE transactions TO `data_analyst@example.com`;
```

### **Step 2: Assigning Schema & Catalog Permissions**
```sql
GRANT USAGE ON SCHEMA finance TO `finance_team`;
GRANT SELECT ON CATALOG enterprise_data TO `data_engineer@example.com`;
```

### **Step 3: Implementing Row-Level Security (RLS)**
```sql
CREATE ROW ACCESS POLICY region_restrict 
ON sales_data
USING (current_user() = 'user@example.com');
```

### **Step 4: Enforcing Column-Level Masking for PII Data**
```sql
ALTER TABLE customer_info 
ALTER COLUMN ssn SET MASKING POLICY mask_ssn_policy;
```

---

## **Lab 3: Automating Workspace Setup Using APIs & Terraform**

### **Step 1: Creating a Cluster via API**
```python
import requests
TOKEN = "<DATABRICKS_ACCESS_TOKEN>"
DATABRICKS_URL = "https://<databricks-instance>.cloud.databricks.com/api/2.0/clusters/create"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

cluster_config = {
  "cluster_name": "Production Cluster",
  "spark_version": "11.3.x-scala2.12",
  "node_type_id": "Standard_DS3_v2",
  "num_workers": 5
}

response = requests.post(DATABRICKS_URL, headers=headers, json=cluster_config)
print(response.json())
```

### **Step 2: Assigning Notebook Permissions via API**
```python
notebook_permissions = {
  "access_control_list": [{"user_name": "user@example.com", "permission_level": "CAN_RUN"}]
}
requests.put(f"{DATABRICKS_URL}/api/2.0/permissions/notebooks/<notebook_id>", headers=headers, json=notebook_permissions)
```

### **Step 3: Automating Workspace Setup Using Terraform**
```hcl
resource "databricks_permissions" "finance_table" {
  table = "finance_data"
  access_control {
    user_name = "analyst@example.com"
    permission_level = "CAN_SELECT"
  }
}
```

---

## **Lab 4: Implementing Enterprise-Grade Security Policies**

### **Step 1: Enforcing Multi-Factor Authentication (MFA)**
1. Navigate to **Databricks Account Settings**.
2. Click **Security Settings → Enable MFA**.
3. Require all workspace admins to use **Multi-Factor Authentication**.

### **Step 2: Configuring IP Whitelisting**
Restrict access to Databricks from specific corporate IPs.
```json
{
  "ip_access_list": [
    {"ip_address": "192.168.1.1/32", "label": "Allowed Office IP"}
  ]
}
```

### **Step 3: Enabling Audit Logging**
1. Go to **Databricks Admin Console → Logs**.
2. Enable **Audit Logging to Azure Monitor or AWS CloudTrail**.
3. Run queries to monitor access patterns.

### **Step 4: Monitoring User Activity**
```sql
SELECT * FROM system.audit_logs WHERE action = 'QUERY_EXECUTED';
```

---

## **Lab 5: Managing Job & Workflow Permissions**

### **Step 1: Creating a Job with User Restrictions**
```python
job_config = {
  "name": "Daily ETL Process",
  "tasks": [{
    "task_key": "load_data",
    "notebook_task": {
      "notebook_path": "/Repos/etl_pipeline"
    },
    "existing_cluster_id": "<Cluster_ID>",
    "permissions": [{"user_name": "analyst@example.com", "permission_level": "CAN_VIEW"}]
  }]
}
requests.post(f"{DATABRICKS_URL}/api/2.0/jobs/create", headers=headers, json=job_config)
```

### **Step 2: Assigning Job Permissions via UI**
1. Navigate to **Jobs → Select Job**.
2. Click **Permissions → Assign Roles**.
3. Grant `CAN_MANAGE`, `CAN_VIEW`, or `CAN_RUN`.

---

## **Conclusion**
These labs provide hands-on experience in:
- **Managing users, groups, and RBAC effectively**.
- **Configuring Unity Catalog for governance & security**.
- **Automating Databricks workspace setup using Terraform & APIs**.
- **Enforcing security best practices across the Databricks environment**.
- **Managing job and workflow permissions dynamically**.

By mastering these labs, you ensure a **secure, compliant, and scalable** Databricks deployment for enterprise-level data processing and analytics.

