import socket
import argparse
import sys
from os import path
import json
from player import Player
from dict_board import Board
from player_strategy import bopHappyStrategy, randomStrategy, smartStrategy

host = 'penghu.eecs.northwestern.edu'
port = 9878


# Connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


while True:
    response = s.recv(4096)
    res = json.loads(response)
    if res == "":
        break

    if res == "name":
        player = Player("team4", smartStrategy())
        request = json.dumps({"name": player.name()}) + "\r\n"
        s.sendall(bytes(request,encoding="utf-8"))
    elif "start-game" in res.keys():
        player.start_game(res["start-game"][0], res["start-game"][1])
        request = json.dumps("okay") + "\r\n"
        s.sendall(bytes(request,encoding="utf-8"))
    elif "take-turn" in res.keys():
        board = Board(res["take-turn"][0]['white'], res["take-turn"][0]['black'])
        turn = player.turn(board, res["take-turn"][1])
        request = json.dumps({"turn": turn}) + "\r\n"
        s.sendall(bytes(request,encoding="utf-8"))
    elif "end-game" in res.keys():
        board = Board(res["end-game"][0]['white'], res["end-game"][0]['black'])
        player.end_game(board, res["end-game"][1])
        request = json.dumps("okay") + "\r\n"
        s.sendall(bytes(request,encoding="utf-8"))
s.close()

    



