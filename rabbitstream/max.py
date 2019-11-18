import pika
import sys 

input_queue = sys.argv[1]
output_queue = sys.argv[2]

conn = pika.BlockingConnection(
	pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue=input_queue)
channel.queue_declare(queue=output_queue)

max_val = -1000000.0
def update_max(ch, method, properties, body):
	global max_val
	
	connection = pika.BlockingConnection(
    	pika.ConnectionParameters('localhost'))
	chan = connection.channel()

	max_val = max(max_val, float(body))
	#print(' [x] max of %d is %d ' % (int(body), max_val))
	
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	chan = connection.channel()	
	chan.basic_publish(
		exchange='',
    	routing_key = output_queue,
    	body = str(max_val))
	
	connection.close()


channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=update_max)

print(input_queue +' ---->  max() ----> ' + output_queue )
channel.start_consuming()
	
