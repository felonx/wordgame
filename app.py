
import random

from referee import Referee
from wordgame import Wordgame
from words import get_all_words

HOST = 'localhost'
PORT = 1883


## TOPICS in our mqtt broker:

#  /REF   - for public messages from REF, all players should subscribe to
#  /REF/answers/{player_name}  - for sending answers from player
#  /REF/response/{player_name} - for sending answer from ref to player
#  /REF/connection - REF listens to, only for initial connection from player

        
if __name__ == '__main__':

    print('loading words...')
    words = get_all_words()
    game = Wordgame(word=random.choice(words), answers=set(words))
    ref = Referee(game=game, client_id='Referee')
    ref.connect(HOST, PORT)
    ref.loop_forever()
