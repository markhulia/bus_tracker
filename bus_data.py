from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time


def read_file(file):
    with open(file, 'r') as f:
        return json.load(f)


def generate_uuid():
    return uuid.uuid4()


def generate_checkpoint(coordinates, producer):
    i = 0
    while i < len(coordinates):
        data = {}
        data['busline'] = '17'
        data['key'] = f"{data['busline']}_{str(generate_uuid())}"
        data['timestamp'] = str(datetime.utcnow())
        data['longitude'] = coordinates[i][0]
        data['latitude'] = coordinates[i][1]
        message = json.dumps(data)
        producer.produce(str(message).encode('ascii'))

        if i == len(coordinates) - 1:
            i = 0
        else:
            i += 1

        time.sleep(1)


def main():
    client = KafkaClient(hosts="0.0.0.0:9092")
    topic = client.topics['busData']
    producer = topic.get_sync_producer()
    raw_data = read_file('data/data_1.json')
    coordinates = raw_data['features'][0]['geometry']['coordinates']
    generate_checkpoint(coordinates, producer)


if __name__ == "__main__":
    main()
