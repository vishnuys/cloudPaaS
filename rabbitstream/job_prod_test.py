import pika
import json

job = {'jobid':1, 'topology':['max','min']}

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn.channel()
channel.queue_declare(queue='job_queue')
channel.basic_publish(exchange='',
					 routing_key = 'job_queue',
					 body = json.dumps(job))
conn.close()
print(" [x] sent job" + json.dumps(job))
