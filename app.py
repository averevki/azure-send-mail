from flask import Flask, request, render_template
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SERVICE_BUS_CONN_STR = os.getenv("SERVICE_BUS_CONN_STR")
QUEUE_NAME = "bussin"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Send email to Service Bus
    with ServiceBusClient.from_connection_string(SERVICE_BUS_CONN_STR) as client:
        with client.get_queue_sender(QUEUE_NAME) as sender:
            message = ServiceBusMessage(json.dumps({"email": request.form['email']}))
            sender.send_messages(message)

    return "Subscription successful!", 200


if __name__ == '__main__':
    app.run()
