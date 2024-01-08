from dict_board import Board
from rule_checker import RuleChecker
from random import randint
from random import seed
from player import Player
import json
from player_strategy import randomStrategy, bopHappyStrategy


class Administrator:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.game_ended = False
        self.replaced = False
        self.turn = 1
        self.board = Board([1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19],
                           [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24])

    # Run Turns between players until game is over
    #@property
    def run_game(self):

        # start game for both players 
        self.player1.start_game("white", self.player2.player_name)
        self.player2.start_game("black", self.player1.player_name)

        if type(self.player2.player_name) != str:
            self.replaced = True
            self.player2 = Player("Malnati", randomStrategy())
            self.player2.start_game("black", self.player1.player_name)

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
                turn = self.player1.turn(self.board, dice)
                for move in turn:
                    self.board.make_move("white", "black", move[1], move[0])

            # Take turn for player 2   
            elif self.turn == 2:
                self.turn = 1
                # if remote player hasn't been replaced
                if not self.replaced:
                    turn = self.player2.turn(self.board, dice)
                    if type(turn) == dict:
                        turn = turn['turn']


                    # Check Move Validity
                    rc = RuleChecker()
                    if turn == "not a move":
                        self.replace_remote(dice)

                    if rc.check_validity("black", dice, turn, self.board):
                        for move in turn:
                            self.board.make_move("black", "white", move[1], move[0])
                    else:
                        self.replace_remote(dice)
                else:
                    turn = self.player2.turn(self.board, dice)
                    for move in turn:
                        self.board.make_move("black", "white", move[1], move[0])

            # check if game over
            if self.board.query(["white", "home"]) == 15:
                self.end_game("white")
                self.game_ended = True
                return self.player1
                break
            if self.board.query(["black", "home"]) == 15:
                self.end_game("black")
                self.game_ended = True
                return self.player2
                break

    def end_game(self, winner):
        if winner == "white":
            self.player1.end_game(self.board, True)
            self.player2.end_game(self.board, False)
        else:
            self.player1.end_game(self.board, False)
            self.player2.end_game(self.board, True)

    def replace_remote(self, dice):
        if not self.replaced:
            self.replaced = True
            self.player2 = Player("Malnati", randomStrategy())
            self.player2.start_game("black", self.player1.player_name)
            turn = self.player2.turn(self.board, dice)
            for move in turn:
                self.board.make_move("black", "white", move[1], move[0])
    

