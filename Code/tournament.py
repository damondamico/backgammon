from TournamentManager import Tournament
import socket
import sys
import json
from player_strategy import randomStrategy
import math


def Log2(x):
    return math.log10(x) / math.log10(2)

contract_checking = True


# Receive Config
config = json.loads(''.join(sys.stdin.readlines()))
num_players = config["players"]
type = config["type"]

# Start Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', config["port"]))
sys.stdout.write(json.dumps("started") + "\n")
sys.stdout.flush()
s.listen(num_players + 5)

# Collect players
connections = []
while len(connections) < num_players:
    c, addr = s.accept()
    connections.append(c)

# Make Network Players
players = []
for c in connections:
    request = json.dumps("name") + "\r\n"
    c.send(bytes(request, encoding="utf-8"))
    response = c.recv(2048)
    if contract_checking:
        from player import PlayerProxy
        network = PlayerProxy(json.loads(response)["name"], False, socket = s, client = c)
    else:
        from networkPlayer import NetworkPlayer
        network = NetworkPlayer(json.loads(response)["name"], s, c)
    players.append(network)

# Start Tournament
if type == "round robin":
    TM = Tournament(players, "round robin", contract_checking)
    records = TM.run_tournament()
    result = json.dumps(records) + "\r\n"
elif type == "single elimination":
    filler_count = 0
    while not (math.ceil(Log2(len(players))) == math.floor(Log2(len(players)))):
        if contract_checking:
            from player import PlayerProxy
            rand = PlayerProxy("Filler" + str(filler_count), strategy = randomStrategy())
        else:
            from player import Player
            rand = Player("Filler" + str(filler_count), randomStrategy())
        filler_count += 1
        players.append(rand)
    TM = Tournament(players, "single elimination", contract_checking)
    winner = TM.run_tournament()
    if "Filler" in winner.player_name:
        result = json.dumps("False") + "\r\n"
    else:
        # winner.disqualify() handled in tournament manager
        result = json.dumps(winner.player_name) + "\r\n"

sys.stdout.write(result)
sys.stdout.flush()
