import csv
import json
import pika
from .models import Job, Result


def store_in_db_cb(ch, method, properties, body):
    dict_body = json.loads(body)
    job = Job.objects.get(id=dict_body['jobid'])
    result = Result(
        job_id=job,
        user_id=job.user,
        max_val=dict_body['max'],
        min_val=dict_body['min'],
        avg_val=dict_body['avg'],
        filepath=dict_body['filepath']
    )
    result.save()


def job_accept_cb(ch, method, properties, body):
    job_acc_msg = json.loads(body)
    job_id = job_acc_msg['jobid']
    job_instance = Job.objects.get(id=job_id)
    output_queue = job_id + '_input'
    result_queue = job_id + '_output'
    with open(job_instance.filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            count += 1
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            chan = connection.channel()
            resp = {'jobid': job_id, 'finalop': json.loads(job_instance.services_order)[-1], 'val': row[job_instance.colname]}
            chan.basic_publish(
                exchange='',
                routing_key=output_queue,
                body=json.dumps(resp))
            connection.close()
        else:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            chan = connection.channel()
            resp = {'jobid': job_id, 'finalop': json.loads(job_instance.services_order)[-1], 'val': 'FINAL'}
            chan.basic_publish(
                exchange='',
                routing_key=output_queue,
                body='FINAL')
            chan.basic_consume(
                queue=result_queue,
                auto_ack=True,
                on_message_callback=store_in_db_cb)

            chan.start_consuming()
