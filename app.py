import paho.mqtt.client as mqtt

from wordgame import Wordgame
from message import Message

HOST = 'localhost'
PORT = 1883


class Referee(mqtt.Client):

    def __init__(self, game: Wordgame, *args, **kwargs):
        self.game = game
        super().__init__(*args, **kwargs)

    def on_connect(self, client, userdata, flags, rc):
        # when a referee connects, he starts listening to the game channel and to players connections
        self.subscribe(topic='wordgame')
        self.subscribe(topic='wordgame_connection')

        # referee publishes to REF topic that each player should listen to
        self.publish(topic='REF', payload='referee is ready')
        print('ref is ready')

    def on_message(self, client, userdata, message):

        msg = Message(message)

        if msg.topic == 'wordgame_connection':
            player_name = msg.data
            self.game.player_joins(player_name)
            self.publish(topic='REF', payload=f'{player_name} joined the game')

        elif message.topic == 'wordgame':
            player_name, guess = msg.data.split(" ", 1)
            response = self.game.player_guess(player_name, guess)
            self.publish(topic='REF', payload=response)
        
        
if __name__ == '__main__':

    game = Wordgame('abrakadabra', set(['abba', 'baba', 'kra', 'kara', 'ar']))
    ref = Referee(game=game, client_id='Referee')
    ref.connect(HOST, PORT)
    ref.loop_forever()
