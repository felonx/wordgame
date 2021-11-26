import time
import sys
import paho.mqtt.client as mqtt

from message import Message

HOST = 'localhost'
PORT = 1883


class Player(mqtt.Client):


    def on_connect(self, client, userdata, flags, rc):
        self.name = str(self._client_id.decode())
        client.subscribe('REF')        
        client.subscribe(f'REF/response/{self.name}')        
        client.publish(topic='REF/connection', payload=self._client_id)
        print('player connected')
        
    def on_message(self, client, userdata, message):
        msg = Message(message)      
        print(msg.data)

    def input_loop(self):
        while True:
            time.sleep(0.5)
            guess = input('enter your guess\n')
            self.publish(topic=f'REF/answers/{self.name}', payload=str(guess))

                

if __name__ == '__main__':

    player = Player(sys.argv[1])
    player.connect(HOST, PORT)
    player.loop_start()
    player.input_loop()
    

    
