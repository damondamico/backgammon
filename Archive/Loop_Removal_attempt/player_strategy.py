from copy import deepcopy
import random
from rule_checker import RuleChecker

class bopHappyStrategy:   
    def __init__(self):
        pass
    def choose_turn(self, board, color, opp_color, dice):
        rc = RuleChecker()
        return rc.get_valid_moves(color, opp_color, dice, board, _score_fun=self._score_fun)

    def _score_fun(self, board_copy, color, opp_color):
        score = 0
        for key in board_copy.board[color].keys():
            if board_copy.board[color][key]:
                score -= board_copy.board[color][key] * board_copy.get_distance(color, key, "home")
            if board_copy.board[opp_color][key]:
                score += board_copy.board[opp_color][key] * board_copy.get_distance(opp_color, key, "home")
        return score

class randomStrategy:
    def __init__(self):
        pass
    def choose_turn(self, board, color, opp_color, dice):
        rc = RuleChecker()
        return rc.get_valid_moves(color, opp_color, dice, board, _score_fun=self._score_fun)

    def _score_fun(self, board_copy, color, opp_color):
        return random.randint(0,100)


class smartStrategy:
    def __init__(self):
        pass
    def choose_turn(self, board, color, opp_color, dice):
        score = False
        optimalTurn = []
        if self.first_turn(board) and len(dice) < 4:
            return self.openings(dice, color)
        else:
            rc = RuleChecker()
            return rc.get_valid_moves(color, opp_color, dice, board, _score_fun=self._score_fun)


    def _score_fun(self, board_copy, color, opp_color):
        score = 0
        for key in board_copy.board[color].keys():
            val = board_copy.board[color][key]
            opp_val = board_copy.board[opp_color][key]
            if val:
                score -= val * board_copy.get_distance(color, key, "home")
                # Discourage blots
                if val == 1:
                    score -=1
                # Discourage candlesticks
                elif val > 3:
                    score -= 1
            elif opp_val:
                score += opp_val * board_copy.get_distance(opp_color, key, "home")
        return score

    def first_turn(self, board):
        starting_board = {
            'black': {"bar": 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 5, 7: 0, 8: 3, 9: 0, 10: 0, 11: 0, 12: 0, 13: 5, 14: 0,
                      15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 2, "home": 0},
            "white": {"bar": 0, 1: 2, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 5, 13: 0, 14: 0,
                      15: 0, 16: 0, 17: 3, 18: 0, 19: 5, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, "home": 0}}
        if board.board == starting_board:
            return True
        else:
            return False

    def openings(self, dice, color):
        white_moves = {"[2, 1]": [[1, 2], [12, 14]],
                       "[3, 1]": [[17, 20], [19, 20]],
                       "[3, 2]": [[1, 4], [12, 14]],
                       "[4, 1]": [[1, 2], [12, 16]],
                       "[4, 2]": [[17, 21], [12, 14]],
                       "[4, 3]": [[1, 5], [12, 15]],
                       "[5, 1]": [[1, 2], [12, 17]],
                       "[5, 2]": [[12, 14], [12, 17]],
                       "[5, 3]": [[17, 22], [19, 22]],
                       "[5, 4]": [[1, 5], [12, 17]],
                       "[6, 1]": [[12, 18], [17, 18]],
                       "[6, 2]": [[1, 7], [12, 14]],
                       "[6, 3]": [[1, 7], [12, 15]],
                       "[6, 4]": [[1, 7], [12, 16]],
                       "[6, 5]": [[1, 7], [7, 12]],}
        black_moves = {"[2, 1]": [[24, 23], [13, 11]],
                       "[3, 1]": [[8, 5], [6, 5]],
                       "[3, 2]": [[24, 21], [13, 11]],
                       "[4, 1]": [[24, 23], [13, 9]],
                       "[4, 2]": [[8, 4], [6, 4]],
                       "[4, 3]": [[24, 20], [13, 10]],
                       "[5, 1]": [[24, 23], [13, 8]],
                       "[5, 2]": [[13, 11], [13, 8]],
                       "[5, 3]": [[8, 3], [6, 3]],
                       "[5, 4]": [[24, 20], [13, 8]],
                       "[6, 1]": [[13, 7], [8, 7]],
                       "[6, 2]": [[24, 18], [13, 11]],
                       "[6, 3]": [[24, 18], [13, 10]],
                       "[6, 4]": [[24, 18], [13, 9]],
                       "[6, 5]": [[24, 18], [18, 13]],}

        s = repr(sorted(dice, reverse=True))
        if color == "white":
            return white_moves[s]
        else:
            return black_moves[s]
