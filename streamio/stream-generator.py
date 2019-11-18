from kafka import KafkaProducer
from time import sleep

producer = KafkaProducer(bootstrap_servers='localhost:9092')
for _ in range(10):
	producer.send('input_first', b'this is a message') 

producer.close()
