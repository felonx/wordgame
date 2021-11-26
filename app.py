import paho.mqtt.client as mqtt
import random

from wordgame import Wordgame
from message import Message
from words import get_all_words

HOST = 'localhost'
PORT = 1883


## TOPICS in our mqtt broker:

#  /REF   - for public messages from REF, all clients should subscribe to
#  /REF/_answers/{player_name}  - for sending answers from player
#  /REF/_response/{player_name} - for sending answer from ref to player
#  /wordgame_connection - REF listens to, only for initial connection from player


class Referee(mqtt.Client):

    def __init__(self, game: Wordgame, *args, **kwargs):
        self.game = game
        super().__init__(*args, **kwargs)

    def on_connect(self, client, userdata, flags, rc):
        
        print('referee is connecting to server')
        
        # when a referee connects, he starts listening to the game channel and to players connections
        self.subscribe(topic='wordgame_connection')

        # referee publishes to REF topic that each player should listen to
        self.publish(topic='REF', payload='referee is ready')
        

      

    def on_message(self, client, userdata, message):

        msg = Message(message)

        print(f'referee received message {msg}')

        if msg.topic == 'wordgame_connection':
            player_name = msg.data            
            self.game.player_joins(player_name)
            self.subscribe(topic=f'REF/_answers/{player_name}')
            print(f'referee now listens to {player_name} answers')
            self.publish(topic='REF', payload=f'{player_name} joined the game')
            self.publish(topic='REF', payload=f'word to play is: {self.game.word.upper()}')

        elif '/_answers/' in message.topic:
            player_name = message.topic.split('/')[-1]            
            response = self.game.player_guess(player_name, msg.data)
            self.publish(topic=f'REF/_response/{player_name}', payload=response)
        
        
        
if __name__ == '__main__':

    words = get_all_words()
    word = random.choice(words)

    game = Wordgame(word, set(words))
    ref = Referee(game=game, client_id='Referee')
    ref.connect(HOST, PORT)
    ref.loop_forever()
