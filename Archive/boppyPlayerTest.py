import sys, json
from dict_board import Board
from player import Player
from player_strategy import bopHappyStrategy

test = json.loads(sys.stdin.read())
b = Board(test[0]['white'], test[0]['black'])
bopPlayer = Player("Rufus", bopHappyStrategy())
bopPlayer.start_game(test[1],"Hank")
res = bopPlayer.turn(b,test[2])
print(json.dumps(res))