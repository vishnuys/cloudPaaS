import pika
import random
import sys
import json

out_queue = sys.argv[1]
job_id = sys.argv[2]
jog_topology = json.loads(sys.argv[3])

job = { 'jobid':job_id, 'topology':job_topology }


conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn.channel()
channel.queue_declare(queue=out_queue)
channel.basic_publish(exchange='',
					 routing_key = out_queue,
					 body = json.dumps(job))
conn.close()
print(" [x] sent 'some messages'  ")
