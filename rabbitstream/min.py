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
min_val = 1000000.0


def update_min(ch, method, properties, body):
    global min_val, last_val
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    chan = connection.channel()

    print (body)
    body_json = json.loads(body)
    val = body_json['val']
    final_op = body_json['finalop']
    print ('Val == FINAL is :')
    print (val == 'FINAL')
    if val == 'FINAL':
        if final_op == 'min':
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
        return

    min_val = min(min_val, float(val))
    body_json['min'] = min_val
    if final_op == 'min':
        last_val = body_json
    # print(' [x] min of %d is %d ' % (int(body), min_val))
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

print(input_queue + ' ---->  min() ----> ' + output_queue)
channel.start_consuming()
