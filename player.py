import time
import sys
import paho.mqtt.client as mqtt
import threading

from message import Message

HOST = 'localhost'
PORT = 1883


class Player(mqtt.Client):


    def on_connect(self, client, userdata, flags, rc):
        self.name = str(self._client_id.decode())
        client.subscribe('REF')        
        client.subscribe(f'REF/_response/{self.name}')        
        client.publish(topic='wordgame_connection', payload=self._client_id)
        print('player connected')
        
    def on_message(self, client, userdata, message):
        msg = Message(message)      
        print(f'{self.name} received message:', msg.topic, msg.data)
        
    def get_input(self, guess):
        self.publish(topic=f'REF/_answers/{self.name}', payload=str(guess))

if __name__ == '__main__':

    player = Player(sys.argv[1])
    player.connect(HOST, PORT)
    player.loop_start()
    while True:
        time.sleep(0.5)
        guess = input('enter your guess\n')
        player.get_input(guess)

    
