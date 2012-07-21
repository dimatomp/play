import argparse
import config_helpers
import pickle
import copy


def get_js(players_cnt):
    import generator
    from tournament_stages.game_signature import GameSignature

    gen = generator.Generator()
    signature = GameSignature(1, 1, 1, 1)
    return gen.generate_start_positions(signature, players_cnt)


def parse_bots_file(filename):
    file_ = open(filename)
    for line in file_:
        yield line.strip()


def create_players(filename):
    import player
    for number, cmd in enumerate(parse_bots_file(filename)):
        yield player.Player(cmd, cmd.split()[-1].split('/')[-1], 'Bot #{}'.format(number))


def play(args):
    from game_simulator import GameSimulator
    from tournament_stages.game_signature import GameSignature
    from bot import ExecuteError

    players = list(create_players(args.bot_commands_file))
    signature = GameSignature(1, 1, 1, 1)
    jury_state = next(get_js(len(players)))
    copied_js = copy.deepcopy(jury_state)
    game = GameSimulator(players, copied_js, signature)
    try:
        game_controller = game.play()
        return game_controller
    except ExecuteError:
        pass


def visualize(game_controller):
    import development_tools.ascii_visualizer as vizualizer
    ascii_viz = vizualizer.AsciiVisualizer(game_controller)
    ascii_viz.activate()


def dump_game_controller(gc, filename=None):
    if not filename:
        print('Would you like to save game log? (y/n)')
        answer = input()
        if answer == 'y':
            print('Enter name of the file')
            filename = input()
        else:
            return
    with open(filename, 'wb') as f:
        f.write(pickle.dumps(gc))


def load_game_controller(filename):
    file_ = open(filename, 'rb')
    obj = pickle.load(file_)
    return obj


def print_final_scores(gc):
    print ('\n\nFinal scores:')
    output = sorted([(score, name) for name, score in gc.get_scores().items()])[::-1]
    for score, name in output:
        print ('{player.bot_name:8s} by '
               '{player.author_name:23s} \t {score}'.format(player=name,
                                                            score=score))
    print('\n\n')


def new_game(args):
    game_controller = play(args)
    if not args.only_run and game_controller:
        if args.visualize:
            visualize(game_controller)
        print_final_scores(game_controller)
        if not args.save_to:
            dump_game_controller(game_controller)
        else:
            dump_game_controller(game_controller, args.save_to)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-c', '--bot-commands-file', required=True,
        help='file where each line represents command to launch bot'
    )

    arg_parser.add_argument(
        '-d', '--directory', required=True,
        help='directory with game'
    )

    arg_parser.add_argument(
        '-v', '--visualize', action='store_true',
        help='visualize game after run'
    )

    arg_parser.add_argument('-s', '--save-to', help='save game log to file')
    arg_parser.add_argument('-f', '--from-file', help='visualize log')
    arg_parser.add_argument(
        '-r', '--only-run', action='store_true',
        help='don\'t visualize and save logs, only run game'
    )

    args = arg_parser.parse_args()

    config_helpers.initialize_game_environment(args.directory)

    if args.from_file:
        game_controller = load_game_controller(args.from_file)
        visualize(game_controller)
    else:
        new_game(args)


if __name__ == '__main__':
    main()
