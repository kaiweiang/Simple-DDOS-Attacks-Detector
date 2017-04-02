from __future__ import print_function
import time
import json
import argparse
import read_apache_log
from kafka import KafkaProducer
from datetime import datetime


def send_message(producer, topic, input):
    #with open('sample_apache_log.txt', 'r') as fo:
    with open(input, 'r') as fo:
        rows = read_apache_log.apache_log_row(fo)
        for message_raw in rows:
            producer.send(topic, json.dumps({'remote_host': message_raw[0],
                                                  'user-identifier': message_raw[1],
                                                  'frank': message_raw[2],
                                                  'time_received': message_raw[3],
                                                  'request_first_line': message_raw[4],
                                                  'status': message_raw[5],
                                                  'size_bytes': message_raw[6],
                                                  'request_header_referer': message_raw[7],
                                                  'request_header_user_agent': message_raw[8]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-rh', '--host', default="127.0.0.1:9092")
    parser.add_argument('-t', '--topic', default='messages')
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()
    producer = KafkaProducer(bootstrap_servers=args.host)
    start=datetime.now()
    send_message(producer, args.topic, args.input)
    print("Time taken to send all the logs:", datetime.now()-start)