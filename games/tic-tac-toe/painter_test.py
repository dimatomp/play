from jury_state import JuryState
from painter import Painter
from player import Player
import unittest
import random


class PainterTests(unittest.TestCase):
    def test_type(self):
        jury_state = JuryState(list(range(9)))
        jury_state.field[2] = 'X'
        jury_state.field[6] = 'O' 
        current_painter = Painter([Player('c', 'Petya'), Player('c', 'Dmitry Philippov')])
        byte_string = current_painter.paint(jury_state)

if __name__ == '__main__':
    unittest.main()
