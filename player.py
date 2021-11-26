import sys
import paho.mqtt.client as mqtt

from message import Message

HOST = 'localhost'
PORT = 1883


class Player(mqtt.Client):


    def on_connect(self, client, userdata, flags, rc):
        client.subscribe('REF')        
        client.publish(topic='wordgame_connection', payload=self._client_id)
        print('player connected')
        self.name = str(self._client_id.decode())

    def on_message(self, client, userdata, message):
        msg = Message(message)      
        print(msg.topic, msg.data)
        self.get_input()

    def get_input(self):    
        guess = input('enter your guess')
        message = ' '.join([self.name, guess])
        self.publish(topic='wordgame', payload=message)

if __name__ == '__main__':

    player = Player('player1')
    player.connect(HOST, PORT)
    player.loop_forever()