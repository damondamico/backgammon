import json
from contracts import contract
from copy import deepcopy


class BoardProxy:
    @contract
    def __init__(self, white: 'list[N],N==15', black: 'list[N],N==15'):
        self.board = Board(white, black)

    # Make a move on the board according to input list m
    @contract
    def move(self, m: 'list[N],N==3') -> None:
        self.board.move(m)
        return

    # Returns the amount of pieces on the space specified by m
    @contract
    def query(self, m: 'list[N],N==2') -> int:
        return self.board.query[m]

    # dumps board to json
    def board_to_json(self, print_to_json):
        return self.board.board_to_json(print_to_json)

    @contract
    def make_move(self, color : 'str', opponent: 'str', to_pos, from_pos):
        self.board.make_move(color, opponent, to_pos, from_pos)

class Board:

    # Initialize
    def __init__(self, white, black):
        self.board = {
            'black': {"bar": 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                      15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, "home": 0},
            "white": {"bar": 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                      15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, "home": 0}}
        self._make_board_dict(white, black)

    def _make_board_dict(self, white, black):
        for i in range(len(white)):
            self.board["black"][black[i]] += 1
            self.board["white"][white[i]] += 1
        return

    # Make a move on the board according to input list m
    def move(self, m):
        self.board[m[0]][m[1]] -= 1
        self.board[m[0]][m[2]] += 1
        return

    # Returns the amount of pieces on the space specified by m
    def query(self, m):
        return self.board[m[0]][m[1]]

    # dumps board to json
    def board_to_json(self, print_to_json):
        result = {"black": [], "white": []}
        for key in self.board['white']:
            for _ in range(self.board["black"][key]):
                result["black"].append(key)
            for _ in range(self.board["white"][key]):
                result["white"].append(key)
        if print_to_json:
            return json.dumps(result)
        else:
            return result

    def make_move(self, color, opponent, to_pos, from_pos):
        occupants = self.query([opponent, to_pos])
        if occupants and to_pos != "home":
            # bop
            self.move([opponent, to_pos, 'bar'])
            self.move([color, from_pos, to_pos])
        else:
            self.move([color, from_pos, to_pos])
    
    def get_distance(self, color, from_pos, to_pos):
        if color == 'black':
            if from_pos == 'bar':
                from_pos = 25
            if to_pos == 'home':
                to_pos = 0
            if from_pos == 'home':
                from_pos = 0
            if to_pos == 'bar':
                to_pos = 25
            return -1*(int(to_pos)-int(from_pos))
        else:
            if from_pos == 'bar':
                from_pos = 0
            if to_pos == 'home':
                to_pos = 25
            if to_pos == 'bar':
                to_pos = 0
            if from_pos == 'home':
                from_pos = 25
            return (int(to_pos)-int(from_pos))
