import csv
import json
import pika
from .models import Job, Node

def job_accept_cb(ch, method, properties, body):
	job_acc_msg = json.loads(body)
	job_id = job_acc_msg['jobid']
	job_instance = Job.objects.get(id=job_id)
	output_queue = job_id + '_input'
	with open(job_instance.filepath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			print(row)
			connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
			chan = connection.channel() 
			chan.basic_publish(
        		exchange='',
        		routing_key = output_queue,
				body = row[job_instance.colname])
			connection.close()

	
