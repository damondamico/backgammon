## Backgammon
This was a school project, the code was written in 2021 by Damon D'Amico and Rishi Gudivaka.
This is the backend implementation of a Backgammon game engine, in Python.
The game engine sends a JSON representation of the game to the front end, which is not included in this project.

It includes:
* an internal representation of the board that updates each turn
* a rule checker that presents all valid moves, and ensures no player is cheating
* Multiplayer features, like support for network play and a tournament organizer
* 3 difficulty levels of AI opponents
  * Easy: Performs random moves
  * Medium: Will try to mess with the player at any given opportunity
  * Hard: Selects the best move with a score based on how it will block the player, control as much of the board as possible, and get its pieces home.
