import pika
import json
import time
from .config import settings
from .scraper import process_message

def start_consumer():
    print("Connecting to RabbitMQ...")
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    )

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=settings.RABBITMQ_QUEUE)

        def callback(ch, method, properties, body):
            print(f" [x] Received {body}")
            result = process_message(body)
            print(f" [x] Processed result: {result}")

        channel.basic_consume(queue=settings.RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception as e:
        print(f"Failed to connect to RabbitMQ or consumer error: {e}")
        # Retry logic could be added here
        time.sleep(5)
