from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers='172.17.48.181:9092',
                         auto_offset_reset='earliest',
                         consumer_timeout_ms=1000)
consumer.subscribe(['input_final'])
for msg in consumer:
    print(msg.value)
consumer.close()
