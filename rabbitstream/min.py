import pika
import sys 

input_queue = sys.argv[1]
output_queue = sys.argv[2]

conn = pika.BlockingConnection(
	pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue=input_queue)
channel.queue_declare(queue=output_queue)

min_val = 1000000.0
def update_min(ch, method, properties, body):
	global min_val
	
	connection = pika.BlockingConnection(
    	pika.ConnectionParameters('localhost'))
	chan = connection.channel()

	min_val = min(min_val, float(body))
	#print(' [x] min of %d is %d ' % (int(body), min_val))
	
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	chan = connection.channel()	
	chan.basic_publish(
		exchange='',
    	routing_key = output_queue,
    	body = str(min_val))
	
	connection.close()


channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=update_min)

print(input_queue +' ---->  min() ----> ' + output_queue )
channel.start_consuming()
	
