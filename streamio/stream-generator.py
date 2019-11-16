from kafka import KafkaProducer
from time import sleep

producer = KafkaProducer(bootstrap_servers='localhost:9092')
for _ in range(100):
	producer.send('anothertopic', b'this is a message') 
	producer.flush()
	sleep(1)

producer.close()
