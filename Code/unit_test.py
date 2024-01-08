import pytest
from rule_checker import RuleChecker
from dict_board import Board

def test_check_validity():
    board = Board([1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19],
                    [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24])
    rc = RuleChecker()
    assert rc.check_home("white", 1, 1, board) == False
    assert rc.check_validity("white", [1,2], [[1,2],[2,4]], board) == True
    assert rc.check_validity("white", [1,2], [[1,4],[2,3]], board) == False

def test_get_valid_moves_2_moves():
    board = Board([23, 24, 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home'],
                    [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 20, 20])
    rc = RuleChecker()
    assert rc.get_valid_moves('white', 'black', [5,6], board) == [[[23, 'home'],[24,'home']],[[23, 'home'],[24,'home']]]

def test_get_valid_moves_1_move():
    board = Board([23, 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home'],
                    [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 20, 20])
    rc = RuleChecker()
    print(rc.get_valid_moves('white', 'black', [5,6], board))
    assert rc.get_valid_moves('white', 'black', [5,6], board) == [[[23, 'home']],[[23, 'home']]]

def test_get_valid_moves_0_moves():
    board = Board([1, 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home', 'home'],
                    [2, 2, 3, 3, 6, 8, 8, 8, 13, 13, 13, 13, 13, 20, 24])
    rc = RuleChecker()
    assert rc.get_valid_moves('white', 'black', [1,2], board) == []

def test_making_move():
    board = Board([1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19],
                    [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24])
    board.make_move("white", "black", 2, 1)
    assert board.board_to_json(False) == {'black':[6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24], "white":[1, 2, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]}

def test_making_move_bop():
    board = Board([1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19],
                    [2, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24])
    board.make_move("white", "black", 2, 1)
    assert board.board_to_json(False) == {'black':['bar', 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24], "white":[1, 2, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]}


def test_board_query():
    board = Board([1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19],
                    [2, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24])
    assert board.query(['white',1]) == 2