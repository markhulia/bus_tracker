from pykafka import KafkaClient

client = KafkaClient(hosts="0.0.0.0:9092")
topic = client.topics['busData']

producer = topic.get_sync_producer()

producer.produce('bus line 51'.encode('ascii'))


