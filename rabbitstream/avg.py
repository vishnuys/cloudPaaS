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
avg_val = 0
n = 0


def update_min(ch, method, properties, body):
    global avg_val, n, last_val

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    chan = connection.channel()

    body_json = json.loads(body)
    val = body_json['val']
    final_op = body_json['finalop']
    if val == 'FINAL':
        if final_op == 'avg':
            chan.basic_publish(
                exchange='', routing_key=final_queue,
                body=json.dumps(last_val))
        else:
            chan.basic_publish(
                exchange='', routing_key=output_queue,
                body=json.dumps(body_json))
        chan.queue_delete(queue=input_queue)
        connection.close()
        sys.exit()

    avg_val = (n * avg_val + float(val)) / (n + 1)
    n += 1
    body_json['avg'] = avg_val
    if final_op == 'avg':
        last_val = body_json

    # print(' [x] avg of %d is %d ' % (int(body), min_val))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chan = connection.channel()
    chan.basic_publish(
        exchange='',
        routing_key=output_queue,
        body=json.dumps(body_json))

    connection.close()


channel.basic_consume(queue=input_queue,
                      auto_ack=True,
                      on_message_callback=update_min)

print(input_queue + ' ---->  avg() ----> ' + output_queue)
channel.start_consuming()
