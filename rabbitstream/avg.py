import pika
import sys 

input_queue = sys.argv[1]
output_queue = sys.argv[2]

conn = pika.BlockingConnection(
	pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue=input_queue)
channel.queue_declare(queue=output_queue)

avg = 0.0
n = 0
def update_avg(ch, method, properties, body):
	global avg, n
	
	connection = pika.BlockingConnection(
    	pika.ConnectionParameters('localhost'))
	chan = connection.channel()

	avg = (avg*n + float(body))/(n + 1)
	n = n + 1
	#print(' [x] max of %d is %d ' % (int(body), max_val))
	
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	chan = connection.channel()	
	chan.basic_publish(
		exchange='',
    	routing_key = output_queue,
    	body = str(avg))
	
	connection.close()


channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=update_avg)

print(input_queue +' ---->  avg() ----> ' + output_queue )
channel.start_consuming()
	
