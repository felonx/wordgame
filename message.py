import datetime

class Message:

    """representation of message"""

    def __init__(self, mqtt_message):
        self.topic = mqtt_message.topic
        self.data = str(mqtt_message.payload.decode('utf-8'))
        self.time = datetime.datetime.utcnow()
