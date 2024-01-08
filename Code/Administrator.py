from rule_checker import RuleChecker
from random import randint
from random import seed
from player import Player
import json
from player_strategy import randomStrategy, bopHappyStrategy


class Administrator:

    def __init__(self, player1, player2, contract_checking):
        self.player1 = player1
        self.player2 = player2
        self.game_ended = False
        self.turn = 1
        if contract_checking:
            from dict_board import BoardProxy
            self.board = BoardProxy([1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19],
                           [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24])
        else:
            from dict_board import Board
            self.board = Board([1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19],
                           [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24])

    # Run Turns between players until game is over
    def run_game(self):

        # start game for both players 
        self.player1.start_game("white", self.player2.player_name)
        self.player2.start_game("black", self.player1.player_name)

        # result of shape: [winner, cheated?, loser, cheated?]

        # Die Roller
        seed(1)

        # Loop Taking Turns
        while not self.game_ended:

            # Dice Rolling
            first = randint(1, 6)
            second = randint(1, 6)
            if first == second:
                dice = [first, first, first, first]
            else:
                dice = [first, second]

            # Take turn for player 1
            if self.turn == 1:
                self.turn = 2
                cheated = self.take_turn(self.player1, "white", "black", dice)
                if cheated:
                    self.end_game(self.player2, self.player1)
                    return [self.player2, False, self.player1, True]

            # Take turn for player 2   
            if self.turn == 2:
                self.turn = 1
                cheated = self.take_turn(self.player2, "black", "white", dice)
                if cheated:
                    self.end_game(self.player1, self.player2)
                    return [self.player1, False, self.player2, True]

            # check if game over
            if self.board.query(["white", "home"]) == 15:
                self.end_game(self.player1, self.player2)
                self.game_ended = True
                return [self.player1, False, self.player2, False]
                break
            if self.board.query(["black", "home"]) == 15:
                self.end_game(self.player2, self.player1)
                self.game_ended = True
                return [self.player2, False, self.player1, False]
                break

    def end_game(self, winner, loser):
        winner.end_game(self.board, True)
        loser.end_game(self.board, False)

    def take_turn(self, player, color, opp_color, dice):
        turn = player.turn(self.board, dice)

        if type(turn) == dict:
            turn = turn['turn']

        # Check Move Validity
        rc = RuleChecker()
        if turn == "not a move":
            return True

        if rc.check_validity(color, dice, turn, self.board):
            for move in turn:
                self.board.make_move(color, opp_color, move[1], move[0])
            return False
        else:
            return True
