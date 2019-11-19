import pika
import random
import sys
from time import sleep

out_queue = sys.argv[1]
min_val = int(sys.argv[2])
max_val = int(sys.argv[3])
delay = float(sys.argv[4])
num_messages = int(sys.argv[5])

for i in range(num_messages):
	random.seed(i)
	conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = conn.channel()
	channel.queue_declare(queue=out_queue)
	rand_val = random.randint(min_val,max_val)
	print (rand_val)
	channel.basic_publish(exchange='',
					 routing_key = out_queue,
					 body = str(rand_val))
	conn.close()
	sleep(delay)

print(" [x] sent 'some messages'  ")
#conn.close()
