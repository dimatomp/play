import random
import copy
from jury_state import JuryState

_field_size = 50


class Generator:
    def generate_players(self, field, players_count):
        new_field = copy.deepcopy(field)
        for player in range(players_count):
            player_x = random.randint(0, _field_size)
            player_y = random.randint(0, _field_size)
            while(new_field[player_x][player_y] != 0):
                player_x = random.randint(0, _field_size)
                player_y = random.randint(0, _field_size)
            new_field[player_x][player_y] = player + 1
        return new_field

    def generate_bullets(self, field, bullets_count):
        new_field = copy.deepcopy(field)
        for bullet in range(bullets_count):
            bullet_x = random.randint(0, _field_size)
            bullet_y = random.randint(0, _field_size)
            while(new_field[bullet_x][bullet_y] != 0):
                bullet_x = random.randint(0, _field_size)
                bullet_y = random.randint(0, _field_size)
            new_field[bullet_x][bullet_y] = -1
        return new_field

    def generate_start_position(self, game_signature, players_count):
        self.players_count = players_count
        '''Generates a list of start positions'''
        random.seed()
        self.bullets_count = self.players_count * 5
        self.time = self.players_count * randint(40, 60)
        for game in range(players_count):
            field = [[0 for i in range(_field_size)]
                for j in range(_field_size)]
            field = generate_players(field, self.players_count)
            field = generate_bullets(field, self.bullets_count)
            yield JuryState(_field_size, field, self.time)
