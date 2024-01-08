from dict_board import Board
from copy import deepcopy
import random
from contracts import contract
from rule_checker import RuleChecker
from networkPlayer import NetworkPlayer

class PlayerProxy:
    @contract
    def __init__(self, name : 'str', strategy = False, socket = False, client = False):
        if strategy:
            self.player = Player(name, strategy)
        else:
            self.player = NetworkPlayer(name, socket, client)
    
    def name(self):
        return self.player.name()

    def start_game(self, color, opp_name):
        self.player.start_game(color, opp_name)
    
    def disqualify(self):
        pass

    @contract
    def turn(self, board, dice : 'list[N](int), 2<=N, N<=4'):
        return self.player.turn(board, dice)

    def end_game(self, board, won : 'bool'):
        self.player.end_game(board, won)




class Player:
    
    def __init__(self, name, strategy):
        self.player_name = name
        self.game_started = False
        self.strategy = strategy
        self.color = None
        self.opp_color = None
    
    def name(self):
        return self.player_name

    def start_game(self, color, opp_name):
        if not self.game_started:
            # Set color
            self.color = color
            # Set opponent info
            self.opp_name = opp_name
            if color == "black":
                self.opp_color = "white"
            else:
                self.opp_color =  "black"
            # Start game
            self.game_started = True
        else:
            print("Tried to start a game with another game already started")
            return
    
    def disqualify(self):
        pass

    def turn(self, board, dice):
        if self.game_started:
            #print("valid turns returned:", valid_turns)
            optimalTurn = self.strategy.choose_turn(board, self.color, self.opp_color, dice)
            return optimalTurn
        else:
            print("Tried to take a turn with no active game")
            return []

    def end_game(self, board, won):
        if self.game_started:
            self.board = board
            self.won = won
            self.game_started = False
        else:
            print("Tried to end a game with no active game.")
            return