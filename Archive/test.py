import sys, json
from board import board

test = json.loads(sys.stdin.read())
if "ends-with-board" in test:
    data = test["ends-with-board"]
    b = board(data[0]['white'], data[0]["black"])
    for move in data[1:]:
        b.move(move)
    print(b.display_board())
elif "ends-with-query" in test:
    data = test['ends-with-query']
    query = data.pop()
    b = board(data[0]["white"], data[0]["black"])
    for move in data[1:]:
        b.move(move)
    print(b.query(query))

