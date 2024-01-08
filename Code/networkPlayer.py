from rule_checker import RuleChecker
import socket
import argparse
import sys
from os import path
import json
from dict_board import Board


class NetworkPlayer():

    def __init__(self, name, socket, client):
        self.socket = socket
        self.player_name = name
        self.client = client

    def start_game(self, color, opp_name):
        request = json.dumps({"start-game": [color, opp_name]}) + "\r\n"
        self.client.sendall(bytes(request, encoding="utf-8"))
        response = json.loads(self.client.recv(4096))
        return response

    def turn(self, board, dice):
        board = board.board_to_json(False)
        request = json.dumps({"take-turn": [board, dice]}) + "\r\n"
        self.client.sendall(bytes(request, encoding="utf-8"))
        response = json.loads(self.client.recv(4096))
        return response

    def end_game(self, board, won):
        board = board.board_to_json(False)
        request = json.dumps({"end-game": [board, won]}) + "\r\n"
        self.client.sendall(bytes(request, encoding="utf-8"))
        response = self.client.recv(4096)

    def disqualify(self):
        request = "\r\n"
        self.client.sendall(bytes(request, encoding="utf-8"))
        self.client.close()
