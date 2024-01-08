import socket
import sys
import json

from player import Player
from Administrator import Administrator
from player_strategy import randomStrategy, bopHappyStrategy
from networkPlayer import NetworkPlayer


class Tournament:
    def __init__(self, players, t_type, contract_checking = False):
        self.players = players
        self.t_type = t_type
        self.scheduler = None
        self.contract_checking = contract_checking

    def run_tournament(self):
        if self.t_type == "round robin":
            self.scheduler = RR_Scheduler(self.players)
            return self.scheduler.schedule()
        elif self.t_type == 'single elimination':
            self.scheduler = SE_Scheduler(self.players)
            return self.scheduler.schedule()


# Round Robin Scheduler
class RR_Scheduler:
    def __init__(self, players, contract_checking):
        self.players = players
        # Holds records by index of player in player list
        self.records = {}
        self.n_games = 0
        self.max_games = 0.5 * len(players) * (len(players) - 1)
        self.contract_checking = contract_checking

    # Run games and return winner
    def schedule(self):
        for player in self.players:
            # w tracks wins, l tracks losses, cheater tracks if player is a cheater
            # opps beaten tracks all opponents beaten for adjusting if a player cheats
            # Each player's records stored as a sub dictionary
            self.records[player] = {'w': 0, 'l': 0, 'cheater': False, 'opps_beaten': []}

        players = self.players

        # Check if odd
        if len(players) % 2:
            players.append(Player('dummy', randomStrategy()))

        while self.n_games < self.max_games:
            # run round
            self.round(players)

            # rotate list
            players = [players[0]] + players[2:] + players[1:2]

        return self.display_records()

    def round(self, players):
        n = len(players)
        # i is forward ptr, j is backward ptr
        for i in range(int(n/2)):
            j = n - i - 1
            player1 = players[i]
            player2 = players[j]
            # dummy player is a bye
            if "dummy" in player1.player_name or "dummy" in player2.player_name:
                continue
            # Both are cheaters, both lose
            elif self.records[player1]['cheater'] and self.records[player2]['cheater']:
                self.records[player1]['l'] += 1
                self.records[player2]['l'] += 1
                self.n_games += 1
            # Player 1 is a cheater, P2 auto wins
            elif self.records[player1]['cheater']:
                self.records[player2]['w'] += 1
                self.records[player2]['opps_beaten'].append(player1)
                self.records[player1]['l'] += 1
                self.n_games += 1
            # Player 2 is a cheater, P1 auto wins
            elif self.records[player2]['cheater']:
                self.records[player1]['w'] += 1
                self.records[player1]['opps_beaten'].append(player2)
                self.records[player2]['l'] += 1
                self.n_games += 1
            # both real players, play game
            else:
                manager = Administrator(player1, player2, contract_checking)
                results = manager.run_game()
                winner = results[0]
                loser = results[2]

                # Record scores
                self.records[winner]['w'] += 1
                self.records[winner]['opps_beaten'].append(loser)
                self.records[loser]['l'] += 1
                self.n_games += 1

                # Check for cheating
                if results[3]:
                    # Loser cheated
                    self.handle_cheating(loser)
                if results[1]:
                    # Winner cheated
                    self.handle_cheating(winner)

    # Output records in output specified list format
    def display_records(self):
        res = []
        for player in self.records.keys():
            record = [player.player_name, self.records[player]['w'], self.records[player]['l']]
            res.append(record)
            # Only connections still active are non-cheaters
            if not self.records[player]['cheater']:
                player.disqualify()
        return res

    # Stops connection and adjusts records if a player is DQ'ed for cheating
    def handle_cheating(self, player):
        player.disqualify()
        self.records[player]['cheater'] = True
        # Remove past wins
        for opp in self.records[player]['opps_beaten']:
            self.records[player]['w'] -= 1
            self.records[player]['l'] += 1
            # Grant wins to past opponents if they aren't cheaters
            if not self.records[opp]['cheater']:
                self.records[opp]['w'] += 1
                self.records[opp]['l'] -= 1
                self.records[opp]['opps_beaten'].append(player)
            self.records[player]['opps_beaten'].remove(opp)


# Single Elimination Scheduler
class SE_Scheduler:
    def __init__(self, players, contract_checking):
        self.players = players
        self.contract_checking = contract_checking

    # Run games and return winner
    def schedule(self):
        while len(self.players) > 1:
            self.round()

        # Disconnect winner
        self.players[0].disqualify()
        return self.players[0]

    def round(self):
        winners = []
        i = 0
        while i < len(self.players):
            player1 = self.players[i]
            player2 = self.players[i + 1]
            # Pick a random winner (first player) for filler games
            if "Filler" in player1.player_name and "Filler" in player2.player_name:
                winners.append(player1)
            else:
                manager = Administrator(player1, player2, contract_checking)
                results = manager.run_game()
                winners.append(results[0])
                results[2].disqualify()
            i += 2
        self.players = winners
