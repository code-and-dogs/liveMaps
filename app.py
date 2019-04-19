from flask import Flask, jsonify, request, Response, render_template
from pykafka import KafkaClient
from pykafka.common import OffsetType
import json

app = Flask(__name__)

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

@app.route('/')
def index():
    return (render_template('index.html'))

#GET ALL MESSAGES FROM TOPIC
@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()
    def events():
        for i in client.topics[topicname.encode('ascii')].get_simple_consumer(consumer_group="mygroup", auto_offset_reset=OffsetType.LATEST,
    reset_offset_on_start=True):
            yield 'data: {0}\n\n'.format(i.value.decode())
    return Response(events(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
