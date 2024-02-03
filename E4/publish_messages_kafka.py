# Import required libraries
from faker import Faker
from time import sleep
import random
import uuid
from datetime import datetime
from kafka_schema_registry import prepare_producer

# Configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:7092']
SCHEMA_REGISTRY_URL = 'http://localhost:8081'
TOPIC_NAME = 'orders'
NUM_MESSAGES = 5
SLEEP_INTERVAL = 1

# Avro Schema
SAMPLE_SCHEMA = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "order_value", "type": "string"},
        {"name": "priority", "type": "string"},
        {"name": "order_date", "type": "string"},
        {"name": "customer_id", "type": "string"},
        {"name": "ts", "type": "string"},
        {"name": "OP", "type": "string"}  # Add the 'OP' column to the Avro Schema
    ]
}

# Kafka Producer
producer = prepare_producer(
    KAFKA_BOOTSTRAP_SERVERS,
    SCHEMA_REGISTRY_URL,
    TOPIC_NAME,
    1,
    1,
    value_schema=SAMPLE_SCHEMA,
)

# Faker instance
faker = Faker()


class DataGenerator:
    @staticmethod
    def get_orders_data(order_id_counter, operation='I'):
        """
        Generate and return a dictionary with mock order data.
        :param order_id_counter: The counter for generating order_id
        :param operation: The operation type ('I' for insert, 'U' for update, 'D' for delete)
        """
        return {
            "order_id": str(order_id_counter),
            "name": faker.text(max_nb_chars=20),
            "order_value": str(random.randint(10, 1000)),
            "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "order_date": faker.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
            "customer_id": str(uuid.uuid4()),
            "ts": str(datetime.now().timestamp()),
            "OP": operation  # Add the 'OP' column with the specified operation type
        }

    @staticmethod
    def produce_avro_message(producer, topic, data):
        """
        Produce an Avro message and send it to the Kafka topic.
        """
        producer.send(topic, data)


def insert_messages_into_kafka(NUM_MESSAGES=20):
    for order_id_counter in range(1, NUM_MESSAGES + 1):
        # Use random.choice to select a random operation type ('I', 'U', or 'D')
        operation_type = random.choice(['I'])
        order_data = DataGenerator.get_orders_data(order_id_counter, operation=operation_type)
        print(order_data)
        DataGenerator.produce_avro_message(producer, TOPIC_NAME, order_data)
        print("Order Payload:", order_data)
        sleep(SLEEP_INTERVAL)


def manual_update():
    order_data = {
        "order_id": "1",
        "name": "update",
        "order_value": "403",
        "priority": "HIGH",
        "order_date": "2024-01-12",
        "customer_id": "cbf2fbf3-28ec-4a10-b440-8dec92058a45",
        "ts": "1706990102.606425",
        "OP": "I"
    }
    DataGenerator.produce_avro_message(producer, TOPIC_NAME, order_data)
    print("Order Payload:", order_data)
    sleep(SLEEP_INTERVAL)

# Call the function to insert messages into Kafka
# insert_messages_into_kafka(NUM_MESSAGES)
manual_update()