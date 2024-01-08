import json
from contracts import contract
from copy import deepcopy
class board:

    # Initialize
    @contract
    def __init__(self, white : 'list[N],N==15', black : 'list[N],N==15'):
        self.white = white
        self.black = black

    # Custom sorting function that puts bar at front and home at end
    def sort_helper(self, x):
        if x == "bar":
            return 0
        elif x == "home":
            return 25
        else:
            return x

    # Make a move on the board according to input list m
    @contract
    def move(self, m : 'list[N],N==3') -> None:
        if m[0] == "black":
            self.black.remove(m[1])
            self.black.append(m[2])
            new_black = sorted(self.black, key = lambda value : self.sort_helper(value))
            self.black = new_black
        elif m[0] == "white":
            self.white.remove(m[1])
            self.white.append(m[2])
            new_white = sorted(self.white, key = lambda value : self.sort_helper(value))
            self.white = new_white

        return

    # Returns the amount of pieces on the space specified by m
    @contract
    def query(self, m : 'list[N],N==2') -> int:
        if m[0] == "black":
            return self.black.count(m[1])
        elif m[0] == "white":
            return self.white.count(m[1])

    # dumps board to json and prints to stdout
    def display_board(self) -> list:
        d = {}
        d["black"] = self.black
        d["white"] = self.white
        return json.dumps(d)
    
    # Checks if a turn is valid then moves if it is, otherwise returns false
    def take_turn(self, color, dice, turn):
        # check if there is a roll for each move
        if color == 'black':
            opponent = 'white'
        else:
            opponent = 'black'
        
        if turn == []:
            for die in dice:
                if color == 'black':
                    for checker in self.black:
                        if checker == "home":
                            continue
                        if self.check_move(color, opponent, die, checker, self.calc_move(color, checker, die)):
                            return False
                else:
                    for checker in self.white:
                        if checker == "home":
                            continue
                        if self.check_move(color, opponent, die, checker, self.calc_move(color, checker, die)):
                            return False
            return self.display_board

        used_dice = 0
        if len(turn) < len(dice):
            dice_copy = deepcopy(dice)
            board_copy = board(deepcopy(self.white), deepcopy(self.black))

        for i in range(len(turn)):
            from_pos = turn[i][0]
            to_pos = turn[i][1]
            distance = self.get_distance(color, from_pos, to_pos)
            #print(distance)
            valid = False

            # match dice rolls to moves
            for j in range(len(dice)):
                #print('dice[j]: ', dice[j])
                if dice[j] == distance:
                    #print('match')
                    roll = dice.pop(j)
                    # check validity
                    valid = self.check_move(color, opponent, roll, from_pos, to_pos)
                    break
                elif dice[j] > distance and to_pos == "home":
                    if self.check_home(color):
                        #print('check if max die works', dice[j])
                        #print(max(self.black))
                        if color == 'black':
                            #print('from: ', from_pos)
                            check = [i for i in self.black if i not in ["bar", "home"]]
                            if max(check) == from_pos:
                                valid = True
                                roll = dice.pop(j)
                                break
                        elif color == 'white':
                            check = [i for i in self.white if i not in ["bar", "home"]]
                            if min(check) == from_pos:
                                # print('true')
                                valid = True
                                roll = dice.pop(j)
                                break

            
            # If move is valid, make move
            if valid:
                used_dice += 1
                self.make_move(color, opponent, to_pos, from_pos)
            else:
                #print('invalid move')
                return False
                    
        # At the end return the board
        if len(dice) != 0:
            max_dice = board_copy.max_usable_dice(color, opponent, dice_copy)
            if used_dice < max_dice:
                return False
            """             # if self.check_valid_moves(color, opponent, dice) > len(turn):
            #     return False
            #print('leftover moves')
            #print(dice)
            for die in dice:
                if color == 'black':
                    for checker in self.black:
                        if checker == "home":
                            continue
                        if self.check_move(color, opponent, die, checker, self.calc_move(color, checker, die)):
                            #print('found valid move')
                            #print(color, die, checker, self.calc_move(color, checker, die))
                            return False
                else:
                    for checker in self.white:
                        if checker == "home":
                            continue
                        if self.check_move(color, opponent, die, checker, self.calc_move(color, checker, die)):
                            #print('found valid move', checker, die, self.calc_move(color, checker, die))
                            return False """
        return self.display_board()

    def check_home(self, color):
        #print('checking home moves')
        if color == 'black':
            home_board = [6,5,4,3,2,1,"home"]
            home_sum = 0
            for pos in home_board:
                home_sum += self.query([color, pos])
            if home_sum == 15:
                return True
        if color == 'white':
            home_board = [19,20,21,22,23,24,"home"]
            home_sum = 0
            for pos in home_board:
                home_sum += self.query([color, pos])
            if home_sum == 15:
                return True

    def check_move(self, color, opponent, roll, from_pos, to_pos):
        # Check if the distance moved is valid with the roll
        distance = self.get_distance(color, from_pos, to_pos)
        if distance < 1:
            return False
        if self.query([color, "bar"]) != 0 and from_pos != "bar":
            return False
        if to_pos != 'home':
            if distance == roll:
                if self.query([color, from_pos]):
                    occupants = self.query([opponent, to_pos])
                    if occupants < 2:
                        return True
        else:
            # check if possible to move home
            return self.check_home(color)
        #print('default false from check')
        return False
    
    
    def make_move(self, color, opponent, to_pos, from_pos):
        occupants = self.query([opponent, to_pos])
        if occupants and to_pos != "home":
            #bop
            self.move([opponent, to_pos, 'bar'])
            self.move([color, from_pos, to_pos])
        else:
            self.move([color, from_pos, to_pos])
    
    def get_distance(self, color, from_pos, to_pos):
        if color == 'black':
            if from_pos == 'bar':
                from_pos = 25
            if to_pos == 'home':
                to_pos = 0
            if from_pos == 'home':
                from_pos = 0
            if to_pos == 'bar':
                to_pos = 25
            return -1*(int(to_pos)-int(from_pos))
        else:
            if from_pos == 'bar':
                from_pos = 0
            if to_pos == 'home':
                to_pos = 25
            if to_pos == 'bar':
                to_pos = 0
            if from_pos == 'home':
                from_pos = 25
            return (int(to_pos)-int(from_pos))

    def calc_move(self, color, pos, die):
        if color == 'white':
            if pos == 'bar':
                pos = 0
            if pos == 'home':
                pos = 25
            target = pos+die
            if target > 24:
                return "home"
            elif target <= 0:
                return "bar"
            else:
                return target
        else:
            if pos == 'bar':
                pos = 25
            if pos == 'home':
                pos = 0
            target = pos - die
            if target <= 0:
                return "home"
            elif target > 24:
                return "bar"
            else:
                return target
        # if opp == 'add':
        #     return pos + die
        # elif opp == 'sub':
        #     return pos - die

    def max_usable_dice(self, color, opponent, dice):
        usable_dice = 0
        for die in dice:
                if color == 'black':
                    for checker in self.black:
                        if checker == "home":
                            continue
                        if self.check_move(color, opponent, die, checker, self.calc_move(color, checker, die)):
                            board_copy = board(deepcopy(self.white), deepcopy(self.black))
                            target = board_copy.calc_move(color, checker, die)
                            board_copy.move([color,checker,target])
                            dice_copy = deepcopy(dice)
                            dice_copy.remove(die)
                            usable_dice = max(usable_dice, 1 + board_copy.max_usable_dice(color, opponent, dice_copy))
                else:
                    for checker in self.white:
                        if checker == "home":
                            continue
                        if self.check_move(color, opponent, die, checker, self.calc_move(color, checker, die)):
                            board_copy = board(deepcopy(self.white), deepcopy(self.black))
                            target = board_copy.calc_move(color, checker, die)
                            board_copy.move([color,checker,target])
                            dice_copy = deepcopy(dice)
                            dice_copy.remove(die)
                            usable_dice = max(usable_dice, 1 + board_copy.max_usable_dice(color, opponent, dice_copy))
        
        return usable_dice
    
