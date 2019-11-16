import faust

app = faust.App(
	'hello-world',
	broker='kafka://172.17.48.132:9092',
	value_serializer='raw'
)

input_topic = app.topic('input_hello')
output_topic = app.topic('output_hello')

@app.agent(input_topic)
async def process(stream):
    async for value in stream:
        await output_topic.send(value=value)

