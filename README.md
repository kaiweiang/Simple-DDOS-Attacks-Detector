# Simple DDOS Attacks Detector

### Prerequisite
```Spark Streaming (Python API)```  
```Apache Kafka (Python API)```   
```Python 2.7 or above``` 

### Description
The program is able to identify potential DDOS attack on the fly from a given apache log file input.  
```Producer step```: The log messages are digested and put into Kafka message queue.  
```Consumer step```: The log messages are sent to and read by Spark Streaming.  
```Analysis step```: A simple logic is used to analyze the log messages and detect the potential DDOS attackers by using MapReduce from Apache Spark.

### Apache log message sample 
```155.156.168.116 - - [25/May/2015:23:11:15 +0000] "GET / HTTP/1.0" 200 3557 "-" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))"```  
For more information, please read the [apache log format](https://httpd.apache.org/docs/2.2/logs.html).

### Note
The program is not run at scale. It is done with a single node pseudo cluster. 

### Future step
Make the program scalable.  
Implement more sophisticated algorithm to detect DDOS attackers. 
