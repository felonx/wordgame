import paho.mqtt.client as mqtt

from message import Message
from wordgame import Wordgame


class Referee(mqtt.Client):

    def __init__(self, game: 'Wordgame', *args, **kwargs):
        self.game = game
        super().__init__(*args, **kwargs)

    def on_connect(self, client, userdata, flags, rc):
        
        self.subscribe(topic='REF/connection')
        print('referee is connected to server and waiting for players')
        print(f'word to play is: {self.game.word.upper()}')
        
    def on_message(self, client, userdata, message):

        msg = Message(message)

        print(f'referee received message {msg}')

        if msg.topic == 'REF/connection':
            player_name = msg.data            
            self.game.player_joins(player_name)
            self.subscribe(topic=f'REF/answers/{player_name}')
            print(f'referee now listens to {player_name} answers')
            self.publish(topic='REF', payload=f'{player_name} joined the game')
            self.publish(topic='REF', payload=f'word to play is: {self.game.word.upper()}')

        elif '/answers/' in message.topic:
            player_name = message.topic.split('/')[-1]            
            response = self.game.player_guess(player_name, msg.data)
            self.publish(topic=f'REF/response/{player_name}', payload=response)
            self.publish(topic=f'REF/response/{player_name}', payload=f'\nword to play is: {self.game.word.upper()}')
