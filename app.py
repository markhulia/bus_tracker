from flask import Flask, render_template, Response
from pykafka import KafkaClient

app = Flask(__name__)


def get_kafka_client():
    return KafkaClient(hosts='0.0.0.0:9092')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# Consumer API
@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()

    def events():
        for message in client.topics[topicname].get_simple_consumer():
            yield 'data: {}\n\n'.format(message.value.decode())

    return Response(events(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True)
