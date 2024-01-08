import sys, json
from dict_board import Board
from player import Player
from player_strategy import randomStrategy


test = json.loads(sys.stdin.read())
b = Board(test[0]['white'], test[0]['black'])
randPlayer = Player("Rufus", randomStrategy())
randPlayer.start_game(test[1],"Hank")
res = randPlayer.turn(b,test[2])
print(json.dumps(res))
