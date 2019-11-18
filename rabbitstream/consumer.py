import pika
import sys

input_queue = sys.argv[1]

conn = pika.BlockingConnection(
	pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue=input_queue)

def print_message(ch, method, properties, body):
	print(body)

channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=print_message)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
	
