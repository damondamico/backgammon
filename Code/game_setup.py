from player import Player
from Administrator import Administrator
from player_strategy import randomStrategy, bopHappyStrategy
from networkPlayer import NetworkPlayer
import socket
import sys
import json

#Load Admin Config
config = json.loads(''.join(sys.stdin.readlines()))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', config["port"]))
sys.stdout.write(json.dumps("started") + "\n")
sys.stdout.flush()
s.listen(1)
c, addr = s.accept()

# Setup Local Player
if config["local"] == "Rando":
    local = Player("Lou", randomStrategy())
elif config["local"] == "Bopsy":
    local = Player("Lou", bopHappyStrategy())

# Setup Network Player
# Get name
request = json.dumps("name") + "\r\n"
c.send(bytes(request, encoding="utf-8"))
response = c.recv(1024)
network = NetworkPlayer(json.loads(response)["name"], s, c)
a = Administrator(local, network)

result = a.run_game()
network.client.close()
sys.stdout.write(result)
sys.stdout.flush()
