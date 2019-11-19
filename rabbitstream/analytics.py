import pika
import json
import sys 

input_queue = sys.argv[1]
output_queue = sys.argv[2]

conn = pika.BlockingConnection(
	pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue=input_queue)
channel.queue_declare(queue=output_queue)

output_dict = {}

max_val = -1000000.0
min_val =  1000000.0
avg_val =  0.0
n_val = 0
def update_max(ch, method, properties, body):
	global max_val, min_val, avg_val, n_val

	connection = pika.BlockingConnection(
    	pika.ConnectionParameters('localhost'))
	chan = connection.channel()

	max_val = max(max_val, float(body))
	min_val = min(min_val, float(body))
	avg_val = (n_val * avg_val + float(body)) / (n_val + 1)
	n_val = n_val + 1

	output_dict['val'] = float(body)
	output_dict['max'] = max_val
	output_dict['min'] = min_val
	output_dict['avg'] = avg_val
	#print(' [x] max of %d is %d ' % (int(body), max_val))
	
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	chan = connection.channel()	
	chan.basic_publish(
		exchange='',
    	routing_key = output_queue,
    	body = json.dumps(output_dict))
	
	connection.close()


channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=update_max)

print(input_queue +' ---->  analytics() ----> ' + output_queue )
channel.start_consuming()
	
