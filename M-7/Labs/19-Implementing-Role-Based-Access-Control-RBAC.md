# **Implementing Role-Based Access Control (RBAC) - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **detailed, step-by-step exercises** to implement **Role-Based Access Control (RBAC) in Databricks, Azure, and cloud-based environments**. These labs will cover:
- **Configuring workspace-level access control**.
- **Managing cluster and job permissions**.
- **Implementing RBAC for Unity Catalog and Delta Lake**.
- **Monitoring and auditing role-based access**.

Each lab includes **real-world examples**, **step-by-step instructions**, and **sample configurations** to ensure **secure access management**.

---

## **Lab 1: Configuring Workspace-Level Permissions in Databricks**
### **Objective:**
- Assign user roles to restrict or grant access to **notebooks, dashboards, and workspace assets**.

### **Step 1: Assign a Role in Databricks Workspace**
1. Open **Databricks Workspace** → Navigate to **Admin Console**.
2. Select **User Management**.
3. Choose a user or group and assign a **role**:
   - **Admin**: Full control over the workspace.
   - **Developer**: Can create and run notebooks/jobs.
   - **Viewer**: Read-only access.

### **Step 2: Verify Role Assignment**
- Log in as the assigned user and verify that actions are restricted based on the assigned role.

**Expected Outcome:**
- Users can only perform actions permitted by their assigned roles.

---

## **Lab 2: Managing Cluster-Level Access**
### **Objective:**
- Configure **access control for clusters** to restrict who can attach, manage, or terminate clusters.

### **Step 1: Assign Cluster Permissions**
```python
# Assign cluster-level access to a user
databricks_clusters_permissions {
  cluster_id = "1234-56789-abcde"
  access_control_list = [
    {
      user_name = "data_engineer@databricks.com"
      permission_level = "CAN_MANAGE"
    }
  ]
}
```

### **Step 2: Verify Cluster Access**
- Attempt to start/terminate a cluster as an unauthorized user.

**Expected Outcome:**
- Only authorized users can manage the cluster.

---

## **Lab 3: Implementing RBAC for Jobs**
### **Objective:**
- Assign **permissions for Databricks jobs** to control who can create, run, or manage them.

### **Step 1: Assign Job Permissions Using CLI**
```bash
databricks jobs permissions add --job-id 9876 --access-level CAN_RUN --principal user@example.com
```

### **Step 2: Validate Job Execution**
- Log in as the assigned user and attempt to **run, modify, or delete** the job.

**Expected Outcome:**
- Users can only perform job actions that match their permission level.

---

## **Lab 4: Securing Table Access Using Unity Catalog**
### **Objective:**
- Configure **fine-grained table access** for Delta Lake using Unity Catalog.

### **Step 1: Grant Table Access**
```sql
GRANT SELECT ON TABLE financial_data TO user@example.com;
```

### **Step 2: Verify Restricted Access**
```sql
SELECT * FROM financial_data;
```

- Try querying the table as a **user without SELECT permissions**.

**Expected Outcome:**
- Unauthorized users should be blocked from accessing the table.

---

## **Lab 5: Enforcing Column-Level and Row-Level Security**
### **Objective:**
- Mask sensitive data and enforce **row-level restrictions**.

### **Step 1: Apply Column Masking for Sensitive Data**
```sql
ALTER TABLE customer_info MASKING POLICY mask_ssn ON (ssn) TO role restricted_access;
```

### **Step 2: Restrict Row Access Based on User Role**
```sql
CREATE ROW ACCESS POLICY region_policy
  ON customer_info
  FOR ROWS WHERE region = CURRENT_USER_REGION();
```

**Expected Outcome:**
- Sensitive columns are **masked** for unauthorized users.
- Users only see **data relevant to their role**.

---

## **Lab 6: Auditing and Monitoring RBAC Changes**
### **Objective:**
- Monitor role-based access changes using Databricks audit logs.

### **Step 1: Enable Databricks Audit Logging**
1. Navigate to **Azure Monitor** → Select **Databricks Workspace**.
2. Enable **Audit Logs** and configure **event tracking**.

### **Step 2: Review Access Logs**
- Query **audit logs** to track unauthorized access attempts.

**Expected Outcome:**
- Logs capture **user access events** and **security policy changes**.

---

## **Conclusion**
By completing these **hands-on labs**, you have learned how to:
- **Implement RBAC in Databricks workspaces, clusters, and jobs**.
- **Secure table access using Unity Catalog**.
- **Enforce column- and row-level security** for data protection.
- **Monitor and audit role-based access for compliance**.

These labs provide **real-world experience** in securing **enterprise data environments using RBAC best practices**.

