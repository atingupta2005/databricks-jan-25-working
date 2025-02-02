# **Advanced Encryption and Network Security - Hands-on Labs**

## **Introduction**
This hands-on lab document provides **detailed, step-by-step exercises** for implementing **encryption and network security** in **Databricks and cloud environments**. These labs cover:
- **Encrypting data at rest and in transit**.
- **Configuring secure network access for Databricks**.
- **Implementing private networking and firewall rules**.
- **Managing encryption keys and secrets securely**.

Each lab includes **real-world examples**, **step-by-step instructions**, and **security best practices** to ensure **data confidentiality and protection**.

---

## **Lab 1: Enabling Data Encryption at Rest**
### **Objective:**
- Configure **encryption at rest** for Azure Storage and Databricks.

### **Step 1: Enable Storage Account Encryption**
```bash
az storage account update \
    --name mydatastore \
    --resource-group mygroup \
    --encryption-services blob,file \
    --encryption-key-source Microsoft.Keyvault
```

### **Step 2: Verify Encryption Settings**
```bash
az storage account show --name mydatastore --query "encryption"
```

**Expected Outcome:**
- The storage account is **encrypted using customer-managed keys (CMK)**.

---

## **Lab 2: Encrypting Data in Transit**
### **Objective:**
- Ensure **secure data transmission** using **TLS encryption**.

### **Step 1: Configure Databricks to Use Encrypted JDBC Connections**
```python
spark.read.format("jdbc").option("url", "jdbc:sqlserver://server.database.windows.net:1433;encrypt=true")
```

### **Step 2: Enforce TLS 1.2 for Azure Application Gateway**
```bash
az network application-gateway ssl-policy set \
    --gateway-name myGateway \
    --resource-group mygroup \
    --policy-type Predefined \
    --policy-name AppGwSslPolicy2022
```

**Expected Outcome:**
- **All data transmissions are encrypted using TLS 1.2 or higher**.

---

## **Lab 3: Securing Network Access to Databricks**
### **Objective:**
- Restrict **Databricks workspace access** to specific IP addresses.

### **Step 1: Configure IP Whitelisting for Databricks**
```bash
az network nsg rule create \
    --resource-group mygroup \
    --nsg-name myNSG \
    --name AllowSpecificIP \
    --priority 100 \
    --direction Inbound \
    --source-address-prefixes 10.0.0.0/16 \
    --destination-port-ranges 443 \
    --access Allow
```

### **Step 2: Verify Network Restrictions**
- Attempt to **connect to Databricks from an unauthorized IP**.

**Expected Outcome:**
- **Unauthorized IPs are blocked** from accessing the Databricks workspace.

---

## **Lab 4: Implementing Private Link for Databricks**
### **Objective:**
- Ensure **Databricks traffic remains within a private network**.

### **Step 1: Deploy Databricks Workspace with Private Link**
```bash
az databricks workspace create \
    --name private-databricks \
    --resource-group mygroup \
    --location eastus \
    --enable-no-public-ip
```

### **Step 2: Verify Private Link Configuration**
```bash
az network private-link-resource list --name private-databricks --resource-group mygroup
```

**Expected Outcome:**
- **Databricks workspace is only accessible via private networking**.

---

## **Lab 5: Managing Encryption Keys and Secrets**
### **Objective:**
- Securely **store and retrieve encryption keys and credentials**.

### **Step 1: Store Secrets in Databricks**
```bash
databricks secrets create-scope --scope mysecrets
```
```python
from pyspark.sql import SparkSession
spark.conf.set("fs.azure.account.key.mydatastore.blob.core.windows.net", dbutils.secrets.get(scope="mysecrets", key="storage-key"))
```

### **Step 2: Validate Secure Access**
- Attempt to **access secrets without proper permissions**.

**Expected Outcome:**
- Unauthorized users **cannot retrieve secrets or access sensitive data**.

---

## **Conclusion**
By completing these **hands-on labs**, you have learned how to:
- **Enable encryption for data at rest and in transit**.
- **Secure Databricks workspaces using network policies and private links**.
- **Manage secrets and encryption keys safely**.
- **Enforce security best practices to protect cloud-based data**.

These labs provide **real-world experience** in implementing **enterprise-grade security** for Databricks and cloud environments.

