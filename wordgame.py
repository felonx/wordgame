class Wordgame:

    def __init__(self, word: str, answers: set) -> None:
        self.word = word
        self.answers = answers
        self.players = set()
        self.scores = {}

    def player_joins(self, player):
        print(f'game: {player} joins')
        self.players.add(player)
        if player not in self.scores:  # maybe he is just reconnecting
            self.scores[player] = set()

    def player_guess(self, player, guess):
        if guess in self.answers and set(guess).issubset(self.word):
            self.answers.remove(guess)
            self.scores[player].add(guess)
            print(f'game: {player} guessed.\n {self.scores}\n')
            return f'\n{guess} OK! current score is:\n{self.get_score()}'
        print(f'game: {player} bad guess')
        return 'bad guess'

    def get_score(self):
        score = sorted([(name, len(words)) for name, words in self.scores.items()], key=lambda x: -x[1])
        score = (': '.join(map(str, items)) for items in score)
        return '\n'.join(s for s in score)


