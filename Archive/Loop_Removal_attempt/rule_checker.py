from dict_board import Board
from copy import deepcopy

class RuleChecker:
    def __init__(self):
        pass
    
    # Checks if a turn is valid then moves if it is, otherwise returns false
    def check_validity(self, color, dice, turn, board):
        # check if there is a roll for each move
        if color == 'black':
            opponent = 'white'
        else:
            opponent = 'black'
        
        valid_moves = self.get_valid_moves(color, opponent, dice, board)

        if turn == [] and valid_moves == []:
            return True
        elif turn in valid_moves:
            return True
        else:
            return False


    def check_home(self, color, from_pos, die, board):
        #print('checking home moves')
        if color == 'black':
            home_board = [6,5,4,3,2,1,"home"]
            home_sum = 0
            for pos in home_board:
                home_sum += board.query([color, pos])
            if home_sum == 15:
                if from_pos - die == 0:
                    return True
                else:
                    for pos in home_board[0:-1]:
                        if board.query([color, pos]):
                            if self.calc_move(color, pos, die) != "home":
                                return False
                            elif pos != from_pos and pos - die == 0:
                                return False
                            elif pos > from_pos and self.calc_move(color, pos, die) == 'home':
                                return False
                    return True

        if color == 'white':
            home_board = [19,20,21,22,23,24,"home"]
            home_sum = 0
            for pos in home_board:
                home_sum += board.query([color, pos])
            if home_sum == 15:
                if from_pos + die == 25:
                    return True
                else:
                    for pos in home_board[0:-1]:
                        if board.query([color, pos]):
                            if self.calc_move(color, pos, die) != "home":
                                return False
                            elif pos != from_pos and pos + die == 25:
                                return False
                            elif pos < from_pos and self.calc_move(color, pos, die) == 'home':
                                return False
                    return True
        return False

    def check_move(self, color, opponent, roll, from_pos, to_pos, board):
        # Check if the distance moved is valid with the roll
        distance = board.get_distance(color, from_pos, to_pos)
        if distance < 1:
            return False
        if board.query([color, "bar"]) != 0 and from_pos != "bar":
            return False
        if to_pos != 'home':
            if distance == roll:
                if board.query([color, from_pos]):
                    occupants = board.query([opponent, to_pos])
                    if occupants < 2:
                        return True
        else:
            # check if possible to move home
            return self.check_home(color, from_pos, roll, board)
        #print('default false from check')
        return False

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

    def get_valid_moves(self, color, opponent, dice, board, _score_fun = False):
        if len(dice) < 4:
            valid_turns = self.non_doubles_valid(color, opponent, dice, board, _score_fun)
            return valid_turns
        else:
            valid_turns, best_score, best_turn = self.doubles_valid(color, opponent, dice[0], board, 0, _score_fun)
            if _score_fun == False:
                return valid_turns
            else:
                return best_turn

    def non_doubles_valid(self, color, opponent, dice, board, _score_fun):
        valid_turns = []
        move0counter = 0
        move1counter = 0
        valid_turns0 = []
        valid_turns1 = []
        best_score0 = False
        best_score1 = False
        best_turn0 = None
        best_turn1 = None
        die0_first_moves = self.get_next_moves(color, opponent, dice[0], board)
        #print(die0_first_moves)
        die1_first_moves = self.get_next_moves(color, opponent, dice[1], board)
        #print(die1_first_moves)
        
        if die0_first_moves:
            move0counter = 1
            for move in die0_first_moves:
                board_copy = deepcopy(board)
                board_copy.make_move(color, opponent, move[1], move[0])
                if _score_fun != False and move0counter < 2:
                    score = _score_fun(board_copy, color, opponent)
                    if best_score0 == False:
                        best_score0 = score
                        best_turn0 = [move]
                    elif score > best_score0:
                        best_score0 = score
                        best_turn0 = [move]
                second_moves = self.get_next_moves(color, opponent, dice[1], board_copy)
                #print('first move:', move, "second moves", second_moves)
                if second_moves:
                    best_score0 = False
                    move0counter = 2
                    for second_move in second_moves:
                        new_turn = [move, second_move]
                        if _score_fun != False:
                            board_copy2 = deepcopy(board_copy)
                            board_copy2.make_move(color, opponent, move[1], move[0])
                            score = _score_fun(board_copy2, color, opponent)
                            if best_score0 == False:
                                best_score0 = score
                                best_turn0 = new_turn
                            elif score > best_score0:
                                best_score0 = score
                                best_turn0 = new_turn

                        #print('new turn', new_turn)
                        valid_turns0.append(new_turn)
            if move0counter == 1:
                valid_turns0 = [[move] for move in die0_first_moves]
        
        if die1_first_moves:
            move1counter = 1
            for move in die1_first_moves:
                board_copy = deepcopy(board)
                board_copy.make_move(color, opponent, move[1], move[0])
                if _score_fun != False and move1counter < 2:
                    score = _score_fun(board_copy, color, opponent)
                    if best_score1 == False:
                        best_score1 = score
                        best_turn1 = [move]
                    elif score > best_score1:
                        best_score1 = score
                        best_turn1 = [move]
                second_moves = self.get_next_moves(color, opponent, dice[0], board_copy)
                #print('first move:', move, "second moves", second_moves)
                if second_moves:
                    best_score1 = False
                    move1counter = 2
                    for second_move in second_moves:
                        new_turn = [move, second_move]
                        if _score_fun != False:
                            board_copy2 = deepcopy(board_copy)
                            board_copy2.make_move(color, opponent, move[1], move[0])
                            score = _score_fun(board_copy2, color, opponent)
                            if best_score1 == False:
                                best_score1 = score
                                best_turn1 = new_turn
                            elif score > best_score1:
                                best_score1 = score
                                best_turn1 = new_turn
                        #print('new turn', new_turn)
                        valid_turns1.append(new_turn)
            if move1counter == 1:
                valid_turns1 = [[move] for move in die1_first_moves]
        
        #print('validturns0\n',valid_turns0)
        #print('validturns1\n',valid_turns1)
        #print(valid_turns0+valid_turns1)
        #print(move0counter, move1counter)
        if move0counter == move1counter:
            valid_turns += valid_turns0
            valid_turns += valid_turns1
            if _score_fun != False:
                if best_score0 > best_score1:
                    best_turn = best_turn0
                else:
                    best_turn = best_turn1
        elif move0counter > move1counter:
            valid_turns = valid_turns0
            if _score_fun != False:
                best_turn = best_turn0
        else:
            valid_turns = valid_turns1
            if _score_fun != False:
                best_turn = best_turn1
        
        #print('validturns\n',valid_turns)
        if _score_fun != False:
            return best_turn
        return valid_turns

    def get_next_moves(self, color, opponent, die, board):
        valid_moves = []
        for key in board.board[color].keys():
            if board.board[color][key]:
                target = self.calc_move(color, key, die)
                if self.check_move(color, opponent, die, key, target, board):
                    valid_moves.append([key, target])
        return valid_moves

    

    
    def doubles_valid(self, color, opponent, die, board, movecounter, _score_fun, best_score = False, best_turn = None):
        valid_turns = []
        if movecounter == 4:
            return valid_turns, best_score, best_turn
        next_moves = self.get_next_moves(color, opponent, die, board)
        if next_moves:
            movecounter += 1
            for move in next_moves:
                board_copy = deepcopy(board)
                board_copy.make_move(color, opponent, move[1], move[0])
                next_turns, best_score, best_turn = self.doubles_valid(color, opponent, die, board_copy, movecounter, _score_fun)

                if next_turns:
                    for turn in next_turns:
                        turn.insert(0,move)
                        if _score_fun != False:
                            for move2 in turn:
                                board_copy2 = deepcopy(board_copy)
                                board_copy2.make_move(color, opponent, move2[1], move2[0])
                                score = _score_fun(board_copy2, color, opponent)
                                if score > best_score:
                                    best_score = score
                                    best_turn = turn

                    valid_turns.extend(next_turns)
                else:
                    if _score_fun != False:
                        score = _score_fun(board_copy, color, opponent)
                        if score > best_score:
                            best_score = score
                            best_turn = [move]
                    valid_turns.append([move])
        
        return valid_turns, best_score, best_turn

