import uuid
import json
from datetime import datetime
import time
from flask import Flask, jsonify, request, Response, render_template
from pykafka import KafkaClient

#CREATE FLASK APP
#app = Flask(__name__)
#CORS(app)

#READ JSON DATA into coordinates array
input_file = open ('./data/bus1.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

#CONNECT TO KAFKA CLIENT
def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

#GENERATE UUID
def generate_uuid():
    return uuid.uuid4()

#SEND DATA TO KAFKA TOPIC GEODATA4
def generate_checkpoint(coordinates):
    data = {}
    data['busline'] = '00001'
    client = get_kafka_client()
    topic = client.topics['geodata4'.encode('ascii')]
    producer = topic.get_sync_producer()

    #for coordinate in coordinates:
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        json_data = json.dumps(data)
        print(json_data)
        producer.produce(json_data.encode('ascii'))
        time.sleep(1)

        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1

generate_checkpoint(coordinates)
