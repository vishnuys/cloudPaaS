import os
import pika
import json
import sys

input_queue = sys.argv[1]
output_queue = sys.argv[2]
final_queue = sys.argv[3]

conn = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue=input_queue)
channel.queue_declare(queue=output_queue)
channel.queue_declare(queue=final_queue)


last_message = {}


def store_function(ch, method, properties, body):
    global last_message

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    chan = connection.channel()

    filepath = os.path.join(os.path.dirname(os.path.dirname('__file__')),
                            'interface', 'archive_files', input_queue + '_storage')

    body_json = json.loads(body)
    body_json['filepath'] = filepath

    val = body_json['val']
    final_op = body_json['finalop']
    if final_op == 'storage':
        if val == b'FINAL':
            chan.basic_publish(exchange='', routing_key=final_queue, body=json.dumps(body_json))
            chan.queue_delete(queue=input_queue)
            connection.close()
            sys.exit()

        last_message = body_json

    with open(filepath, 'a') as fp:
        fp.write(json.dumps(body_json))

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chan = connection.channel()
    chan.basic_publish(
        exchange='',
        routing_key=output_queue,
        body=body_json)

    connection.close()


channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=store_function)

print(input_queue + '\t ---->  storage() ----> ' + output_queue)
channel.start_consuming()
