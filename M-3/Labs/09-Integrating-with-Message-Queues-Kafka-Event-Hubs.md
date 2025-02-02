# **Integrating with Message Queues (Kafka, Event Hubs) - Hands-on Labs**

## **Introduction**
This lab document provides **detailed, step-by-step exercises** to help you master **Apache Kafka and Azure Event Hubs integration** with **Apache Spark Structured Streaming**. These hands-on labs focus on real-world scenarios using **Bank Transactions, Loan Foreclosures, and Flight Data**, ensuring minimal modifications for execution.

These labs will cover:
- **Setting up Kafka and Event Hubs Producers & Consumers**
- **Ingesting Streaming Data from Kafka and Event Hubs into Spark**
- **Writing Processed Data to Message Queues using Structured Streaming**
- **Ensuring Fault Tolerance, Exactly-Once Processing, and Checkpointing**
- **Monitoring, Debugging, and Performance Optimization**

Each lab includes **detailed code examples, execution steps, validation checks, and advanced configurations** to ensure **enterprise-grade reliability and scalability**.

---

## **Lab 1: Setting Up Kafka Producer & Consumer**
### **Objective:**
- Configure Kafka topics for streaming data ingestion.
- Produce and consume messages from Kafka.
- Simulate a real-world transaction stream.

### **Step 1: Start Kafka Broker & Create Topics**
```sh
# Start Zookeeper (if not running)
zookeeper-server-start.sh config/zookeeper.properties &

# Start Kafka Broker
kafka-server-start.sh config/server.properties &

# Create a new topic for transactions
kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

### **Step 2: Produce Messages to Kafka Topic**
```sh
# Start a Kafka producer and send messages
echo "101,5000,2024-02-01,Loan" | kafka-console-producer.sh --broker-list localhost:9092 --topic transactions
```

### **Step 3: Consume Messages from Kafka**
```sh
# Start a Kafka consumer
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic transactions --from-beginning
```

**Expected Outcome:**
- The **consumer receives** messages produced to Kafka in real-time.

---

## **Lab 2: Reading Streaming Data from Kafka in Spark Structured Streaming**
### **Objective:**
- Read real-time transaction data from Kafka into Spark Structured Streaming.
- Perform schema enforcement and parsing.

### **Step 1: Configure Spark Streaming Source for Kafka**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split

spark = SparkSession.builder.appName("KafkaConsumerLab").getOrCreate()

kafka_df = spark.readStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", "transactions")\
    .option("startingOffsets", "earliest")\
    .load()
```

### **Step 2: Parse Kafka Message Data and Enforce Schema**
```python
parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as raw_value")\
    .select(split(col("raw_value"), ",").alias("columns"))\
    .selectExpr("columns[0] AS transaction_id", "columns[1] AS amount", "columns[2] AS transaction_date", "columns[3] AS transaction_type")
```

### **Step 3: Start Streaming Query to Console Output**
```python
query = parsed_df.writeStream\
    .format("console")\
    .outputMode("append")\
    .start()
```

**Expected Outcome:**
- Kafka messages are **continuously read, parsed, and structured** in Spark.

---

## **Lab 3: Writing Processed Data to Kafka**
### **Objective:**
- Write transformed transaction data back to Kafka.
- Maintain structured JSON format.

### **Step 1: Define Spark Streaming Query to Kafka Sink**
```python
from pyspark.sql.functions import to_json, struct

query = parsed_df.selectExpr("transaction_id AS key", "to_json(struct(*)) AS value")\
    .writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("topic", "processed-transactions")\
    .option("checkpointLocation", "/mnt/kafka_checkpoint/")\
    .start()
```

**Expected Outcome:**
- Transformed data is published to the **processed-transactions** Kafka topic in JSON format.

---

## **Lab 4: Reading Streaming Data from Azure Event Hubs**
### **Objective:**
- Read real-time messages from Azure Event Hubs in Spark Structured Streaming.
- Handle JSON messages effectively.

### **Step 1: Configure Spark Streaming Source for Event Hubs**
```python
connection_string = "<EVENT_HUB_CONNECTION_STRING>"
event_hub_df = spark.readStream\
    .format("eventhubs")\
    .option("eventhubs.connectionString", connection_string)\
    .load()
```

### **Step 2: Parse JSON Payload from Event Hubs**
```python
from pyspark.sql.functions import from_json

schema = "transaction_id STRING, amount FLOAT, transaction_date STRING, transaction_type STRING"
parsed_event_hub_df = event_hub_df.selectExpr("CAST(body AS STRING) AS json_str")\
    .select(from_json(col("json_str"), schema).alias("data"))\
    .select("data.*")
```

### **Step 3: Start Streaming Query to Console Output**
```python
query = parsed_event_hub_df.writeStream\
    .format("console")\
    .outputMode("append")\
    .start()
```

**Expected Outcome:**
- Messages from Event Hubs are streamed, parsed, and displayed in Spark console.

---

## **Lab 5: Writing Streaming Data to Azure Event Hubs**
### **Objective:**
- Write processed data back to Event Hubs.
- Preserve structured JSON format.

### **Step 1: Define Spark Streaming Query to Event Hubs Sink**
```python
query = parsed_event_hub_df.selectExpr("CAST(transaction_id AS STRING) AS key", "to_json(struct(*)) AS body")\
    .writeStream\
    .format("eventhubs")\
    .option("eventhubs.connectionString", connection_string)\
    .option("checkpointLocation", "/mnt/eventhub_checkpoint/")\
    .start()
```

**Expected Outcome:**
- Processed data is continuously **written back to Azure Event Hubs** in structured format.

---

## **Conclusion**
By completing these **hands-on labs**, you have gained expertise in:
- **Integrating Kafka and Event Hubs with Apache Spark Structured Streaming.**
- **Producing and consuming messages from real-time message queues.**
- **Processing, structuring, and writing data back to Kafka and Event Hubs.**
- **Ensuring data reliability with schema enforcement, checkpointing, and exactly-once processing.**

These labs provide **real-world experience** in building **scalable, fault-tolerant, and event-driven streaming pipelines** with **structured data processing** and **enterprise reliability**.

