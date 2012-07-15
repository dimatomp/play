import random
from jury_state import JuryState


class Generator:
    _max_stones_count = 10
    _games_count = 1

    def generate_start_positions(self, game_signature, players_count):
        '''Generates a list of start positions (Jury states)'''
        for game in range(self._games_count):
            heap_sizes = []
            for heap in range(players_count):
                heap_sizes.append(random.randint(1, self._max_stones_count))
            yield JuryState(heap_sizes)
