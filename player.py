from bot import Bot


class Player:

    def __init__(self, cmd_line, author='John Doe', bot='Some_bot'):
        self.author_name = author
        self.bot_name = bot
        self.path_to_executable = command_line
