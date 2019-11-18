import faust
import sys

app_name = 'hello'
input_topic_str = 'input_first'
output_topic_str = 'input_second'
kafka_broker = 'kafka://localhost:9092'

app = faust.App(
	app_name,
	broker= kafka_broker,
	value_serializer = 'raw',
)

input_topic = app.topic(input_topic_str)
output_topic = app.topic(output_topic_str)

@app.agent(input_topic)
async def process(stream):
    async for value in stream:
        print(value)
        await output_topic.send(value=value)

