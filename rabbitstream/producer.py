import pika
import random
import sys
from time import sleep

out_queue = sys.argv[1]

for i in range(2000):
	random.seed(i)
	conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = conn.channel()
	channel.queue_declare(queue=out_queue)
	rand_val = random.randint(3,1000)
	print (rand_val)
	channel.basic_publish(exchange='',
					 routing_key = out_queue,
					 body = str(rand_val))
	conn.close()
	sleep(0.5)

print(" [x] sent 'some messages'  ")
#conn.close()
