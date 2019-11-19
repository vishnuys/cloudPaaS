import sys
import pika
import json
import subprocess

job_queue = sys.argv[1]

conn = pika.BlockingConnection(
	pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue=job_queue)

def job_message_cb(ch, method, properties, body):
	job_msg = json.loads(body)
	job_id = str(job_msg['jobid'])
	job_operations = job_msg['topology']
	
	print("[message recieved] jobID: " + job_id + " building pipeline --------------------> " + str(job_operations))
	
	input_queue = job_id + '_input'
	output_queue = job_id + '_output'
	
	for i, op in enumerate(job_operations):
		if i == len(job_operations) - 1:
			op_out_queue = output_queue
		else: 
			op_out_queue =  input_queue + '_' + op
		
		command = 'python ' + op + '.py ' + input_queue + ' ' + op_out_queue
		popen_obj = subprocess.Popen(command , shell=True)
		print(popen_obj)

		input_queue = op_out_queue
	
	print("[success] jobID: " + job_id + " pipeline built successfully!")


channel.basic_consume(queue=job_queue,
                      auto_ack=True,
                      on_message_callback=job_message_cb)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
	
