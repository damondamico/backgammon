import sys, json
from dict_board import Board
from rule_checker import RuleChecker

test = json.loads(sys.stdin.read())
b = Board(test[0]['white'], test[0]['black'])
rc = RuleChecker()
valid = rc.check_validity(test[1],test[2],test[3], b)

if valid:
    color = test[1]
    turn = test[3]
    if color == "white":
        opponent = "black"
    else:
        opponent = "white"
    for move in turn:
        to_pos = move[1]
        from_pos = move[0]
        b.make_move(color, opponent, to_pos, from_pos)
    print(b.board_to_json())
else:
    print(json.dumps(False))
