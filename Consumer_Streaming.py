from __future__ import print_function
from pyspark import SparkContext 
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import time
from datetime import datetime
import json
import argparse

def load_msg(msg):
    message = json.loads(msg[1])
    return message['remote_host'], 1

def update_frequency(new_entry, freq_sum):
  if not freq_sum:
    freq_sum = 0
  return sum(new_entry) + freq_sum

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-rh', '--host', default="127.0.0.1:9092")
  parser.add_argument('-t', '--topic', default='messages')
  args = parser.parse_args()
  print('Starting the process...\n')
  start=datetime.now()
  sc = SparkContext(appName="PythonStreamingDirectKafkaDetectDDOS")
  ssc = StreamingContext(sc, 5)
  ssc.checkpoint('checkpoint')
  kvs = KafkaUtils.createDirectStream(ssc, [args.topic], {"metadata.broker.list": args.host})
  parsed = kvs.map(load_msg)  
  updated = parsed.updateStateByKey(update_frequency)
  updated2 = updated.map(lambda (k,v): (str(k), v))
  high_freq = updated2.filter(lambda (k,v): v >= 85)
  high_freq.pprint()
  high_freq.saveAsTextFiles('DDOS_attacker_found_output')
  ssc.start()
  time.sleep(60)
  ssc.stop()
  #ssc.awaitTermination()
  print('Process ended.')
  print('Time taken:', datetime.now()-start)

