import pika
import sys
import json

input_queue = sys.argv[1]
output_queue = sys.argv[2]
final_queue = sys.argv[3]

conn = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue=input_queue)
channel.queue_declare(queue=output_queue)
channel.queue_declare(queue=final_queue)

last_val = {}
max_val = -1000000.0


def update_max(ch, method, properties, body):
    global max_val, last_val
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    chan = connection.channel()

    body_json = json.loads(body)
    val = body_json['val']
    final_op = body_json['finalop']
    if val == b'FINAL':
        if final_op == 'max':
            chan.basic_publish(
                exchange='', routing_key=output_queue,
                body=json.dumps(last_val))
        else:
            chan.basic_publish(
                exchange='', routing_key=final_queue,
                body=json.dumps(body_json))
        chan.queue_delete(queue=input_queue)
        connection.close()
        sys.exit()

    max_val = max(max_val, float(val))
    body_json['max'] = max_val
    if final_op == 'max':
        last_val = body_json
    # print(' [x] max of %d is %d ' % (int(body), max_val))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chan = connection.channel()
    chan.basic_publish(
        exchange='',
        routing_key=output_queue,
        body=json.dumps(body_json))

    connection.close()


channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=update_max)

print(input_queue + ' ---->  max() ----> ' + output_queue)
channel.start_consuming()
