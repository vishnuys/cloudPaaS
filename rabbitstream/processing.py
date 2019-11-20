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

def store_function(ch, method, properties, body):

	connection = pika.BlockingConnection(
    	pika.ConnectionParameters('localhost'))
	chan = connection.channel()
	
	with open(input_queue+'storage','a') as fp:
		fp.write(body.decode())

		
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	chan = connection.channel()	
	chan.basic_publish(
		exchange='',
    	routing_key = output_queue,
    	body = body)
	
	connection.close()


channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=update_)

print(input_queue +' ---->  analytics() ----> ' + output_queue )
channel.start_consuming()
	
